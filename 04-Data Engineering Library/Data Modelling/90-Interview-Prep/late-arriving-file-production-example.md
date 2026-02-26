# Late-Arriving File: Production Example (Bronze -> Silver SCD2 -> Gold)

## Overview
This note shows a production-ready pattern for handling a late-arriving CDC file without metric drift.
It uses:
- Bronze append-only raw ingestion
- Silver canonical historized entity (SCD2 timeline by business key)
- Gold business-facing Type 2 dimension and downstream restatement

Example entity: `event_id` with attributes `event_type`, `status`, `location_id`.

## Core Design Decisions
1. Grain:
- Silver grain: one row per `event_id` version interval (`valid_from`, `valid_to`)
- Gold dimension grain: one row per business version with surrogate key

2. Ordering:
- Business time drives versioning: `source_changed_ts`
- Ingestion time is only tie-breaker and observability metadata

3. Change detection:
- Use `payload_hash` (or full attribute compare) to skip no-op updates
- Do not version rows when only technical metadata changes

4. Timeline integrity:
- Exactly one current row per key
- Non-overlapping validity ranges per key
- Late records may split non-current intervals, not only current row

5. Medallion alignment:
- Bronze preserves source fidelity and replayability
- Silver reconstructs canonical source history
- Gold applies business semantics and serves consumers

## Example Scenario
On `2026-02-25`, file `events_2026_02_25.csv` arrives with changes effective between `2026-01-20` and `2026-01-25`.
Some rows are:
- New keys
- Changes to current versions
- Changes effective in middle of history
- Duplicate/no-op rows
- Delete events (tombstones)

## Step 1: Bronze Raw Append
```sql
insert into bronze.events_raw (
  event_id,
  event_type,
  status,
  location_id,
  op,
  source_changed_ts,
  source_file,
  ingestion_ts
)
select
  payload.event_id,
  payload.event_type,
  payload.status,
  payload.location_id,
  payload.op,
  payload.source_changed_ts,
  'events_2026_02_25.csv' as source_file,
  current_timestamp() as ingestion_ts
from landing.events_2026_02_25;
```

## Step 2: Silver SCD2 Timeline Rebuild (Impacted Keys + Window)
Use a deterministic "rebuild impacted timeline" approach. It is safer than ad-hoc point updates.

### 2.1 Stage and deduplicate incoming rows
```sql
create or replace temporary table stg_events_delta as
select
  event_id,
  event_type,
  status,
  location_id,
  op,
  source_changed_ts,
  ingestion_ts,
  md5(concat_ws('||',
    coalesce(event_type, ''),
    coalesce(status, ''),
    coalesce(location_id, '')
  )) as payload_hash
from (
  select *,
         row_number() over (
           partition by event_id, source_changed_ts, op
           order by ingestion_ts desc
         ) as rn
  from bronze.events_raw
  where source_file = 'events_2026_02_25.csv'
) x
where rn = 1;
```

### 2.2 Identify impacted keys and pull existing Silver history
```sql
create or replace temporary table stg_impacted_keys as
select distinct event_id
from stg_events_delta;

create or replace temporary table stg_existing_hist as
select *
from silver.events_hist
where event_id in (select event_id from stg_impacted_keys);
```

### 2.3 Rebuild complete timeline for impacted keys
```sql
create or replace temporary table stg_rebuilt_timeline as
with unified_changes as (
  -- Existing logical change points
  select
    event_id,
    event_type,
    status,
    location_id,
    cast(false as boolean) as is_delete,
    valid_from as change_ts,
    md5(concat_ws('||',
      coalesce(event_type, ''),
      coalesce(status, ''),
      coalesce(location_id, '')
    )) as payload_hash
  from stg_existing_hist

  union all

  -- New change points from late file
  select
    event_id,
    event_type,
    status,
    location_id,
    case when op = 'D' then true else false end as is_delete,
    source_changed_ts as change_ts,
    payload_hash
  from stg_events_delta
),
ordered as (
  select *,
         row_number() over (
           partition by event_id, change_ts
           order by is_delete asc
         ) as ts_rank
  from unified_changes
),
dedup_at_ts as (
  select *
  from ordered
  where ts_rank = 1
),
remove_noops as (
  select
    event_id,
    event_type,
    status,
    location_id,
    is_delete,
    change_ts as valid_from,
    lead(change_ts) over (
      partition by event_id
      order by change_ts
    ) as next_change_ts,
    payload_hash,
    lag(payload_hash) over (
      partition by event_id
      order by change_ts
    ) as prev_hash
  from dedup_at_ts
),
effective_changes as (
  select *
  from remove_noops
  where prev_hash is null or payload_hash <> prev_hash or is_delete = true
)
select
  event_id,
  event_type,
  status,
  location_id,
  valid_from,
  coalesce(next_change_ts, timestamp '9999-12-31 00:00:00') as valid_to,
  case when next_change_ts is null then true else false end as is_current,
  is_delete,
  payload_hash,
  current_timestamp() as rebuilt_at
from effective_changes;
```

### 2.4 Upsert rebuilt timeline into Silver
```sql
begin;

delete from silver.events_hist
where event_id in (select event_id from stg_impacted_keys);

insert into silver.events_hist (
  event_id, event_type, status, location_id,
  valid_from, valid_to, is_current, is_delete,
  payload_hash, record_source, updated_at
)
select
  event_id, event_type, status, location_id,
  valid_from, valid_to, is_current, is_delete,
  payload_hash, 'bronze.events_raw', rebuilt_at
from stg_rebuilt_timeline;

commit;
```

## Step 3: Gold Type 2 and Restatement
1. Rebuild or incremental-merge `gold.dim_event` from `silver.events_hist` for impacted keys.
2. Restate only impacted Gold marts/facts for affected dates.
3. Publish restatement notice: "`2026-01-20` to `2026-01-25` recalculated due to late file."

```sql
create or replace view gold.dim_event_current as
select *
from gold.dim_event
where is_current = true
  and is_delete = false;
```

Impacted-date restatement pattern:
```sql
create or replace temporary table stg_impacted_dates as
select distinct cast(valid_from as date) as d
from silver.events_hist
where event_id in (select event_id from stg_impacted_keys)
  and valid_from >= timestamp '2026-01-20 00:00:00'
  and valid_from <  timestamp '2026-01-26 00:00:00';

delete from gold.mart_event_daily
where event_date in (select d from stg_impacted_dates);

insert into gold.mart_event_daily (event_date, event_count)
select
  cast(event_ts as date) as event_date,
  count(*) as event_count
from gold.fct_event
where cast(event_ts as date) in (select d from stg_impacted_dates)
group by cast(event_ts as date);
```

## Validation Queries
One current row per key:
```sql
select event_id
from silver.events_hist
where is_current = true
group by event_id
having count(*) <> 1;
```

No overlapping intervals:
```sql
select a.event_id
from silver.events_hist a
join silver.events_hist b
  on a.event_id = b.event_id
 and a.valid_from < b.valid_to
 and b.valid_from < a.valid_to
 and a.valid_from <> b.valid_from
group by a.event_id;
```

Idempotency check after rerun:
```sql
select event_id, valid_from, count(*) as c
from silver.events_hist
group by event_id, valid_from
having count(*) > 1;
```

## Scenarios Covered by This Pattern
1. New key: inserts first version.
2. Latest change: closes old current, inserts new current.
3. Mid-history late change: splits historical interval and adjusts `valid_to`.
4. Older-than-earliest change: inserts new earliest version and shifts next boundary.
5. Duplicate/no-op rows: removed by hash compare and dedup.
6. Delete events: represented as tombstone version (`is_delete = true`).
7. Reprocessing same file: deterministic/idempotent because impacted keys are rebuilt.

## Common Mistakes
1. Updating only `is_current = true` rows for late data.
2. Using ingestion timestamp as business validity timestamp.
3. Treating every file row as a new version (no hash/no-op guard).
4. Recomputing Silver but skipping downstream Gold restatement.

## Practical Checklist
1. Declare grain and business timestamp explicitly.
2. Dedup by key + business time + operation before merge/rebuild.
3. Enforce one-current-row and no-overlap tests.
4. Restate only impacted Gold partitions/marts.
5. Emit restatement metadata for BI consumers.

## Related Notes
- [[scenario-questions]]
- [[late-arriving-data]]
- [[scd-types]]
- [[medallion-architecture]]
