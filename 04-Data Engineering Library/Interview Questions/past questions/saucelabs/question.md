## Input
Source events table columns:
- `event_ts` (timestamp)
- `user_id`
- `service_tier_id`

Assumption: duplicates are exact duplicates on (`event_ts`, `user_id`, `service_tier_id`).

## 1) Deduplicate in the same table (no temp-table swap)
Use `DELETE` + `QUALIFY ROW_NUMBER`:

```sql
DELETE FROM user_tier_events t
USING (
  SELECT event_ts, user_id, service_tier_id
  FROM user_tier_events
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY event_ts, user_id, service_tier_id
    ORDER BY event_ts
  ) > 1
) d
WHERE t.event_ts = d.event_ts
  AND t.user_id = d.user_id
  AND t.service_tier_id = d.service_tier_id;
```

If exact duplicates can still collide on all 3 columns, add a stable ingestion column (for example `load_ts` or `metadata$filename + metadata$file_row_number`) and use that in `ORDER BY`.

## 2) Snowflake dimensional modeling/storage
Use two-layer model:

1. `dim_user_service_tier_hist` (SCD2 history table)
   - `user_id`
   - `service_tier_id`
   - `eff_start_date`
   - `eff_end_date`
   - `active_flag`
   - optional: `record_hash`, `load_ts`, `updated_ts`

2. `dim_user_service_tier_current` (business-friendly current snapshot)
   - `user_id` (unique)
   - `service_tier_id` (latest/current)

Snowflake notes:
- Cluster history table by `(user_id, eff_start_date)` if table is large.
- Use Streams + Tasks or scheduled MERGE for incremental updates.
- Keep raw source immutable if possible (`raw_user_tier_events`) and transform into curated dims.

## 3) SCD explanation and best type here
For tier changes over time, use **SCD Type 2** because you need full history and effective dating.

SCD types:
- Type 0: no changes allowed (static attributes).
- Type 1: overwrite old value (no history).
- Type 2: new row per change with validity dates (full history).
- Type 3: keep limited prior value(s) in extra columns.
- Type 4: current table + separate history table.
- Type 6: hybrid (1+2+3 behaviors).

Best fit here: **Type 2** (or Type 4 physically, while logically still Type 2 behavior).

## 4) CTEs to derive `EFF_START_DATE`, `EFF_END_DATE`, `ACTIVE_FLAG`
```sql
WITH dedup AS (
  SELECT event_ts::timestamp_ntz AS event_ts, user_id, service_tier_id
  FROM user_tier_events
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY event_ts, user_id, service_tier_id
    ORDER BY event_ts
  ) = 1
),
change_points AS (
  SELECT
      event_ts,
      user_id,
      service_tier_id,
      LAG(service_tier_id) OVER (
        PARTITION BY user_id
        ORDER BY event_ts
      ) AS prev_tier
  FROM dedup
),
only_changes AS (
  SELECT event_ts, user_id, service_tier_id
  FROM change_points
  WHERE prev_tier IS NULL OR prev_tier <> service_tier_id
),
scd2 AS (
  SELECT
      user_id,
      service_tier_id,
      event_ts::date AS eff_start_date,
      LEAD(event_ts::date) OVER (
        PARTITION BY user_id
        ORDER BY event_ts
      ) - 1 AS eff_end_date
  FROM only_changes
)
SELECT
    user_id,
    service_tier_id,
    eff_start_date,
    COALESCE(eff_end_date, '9999-12-31'::date) AS eff_end_date,
    CASE WHEN eff_end_date IS NULL THEN 1 ELSE 0 END AS active_flag
FROM scd2;
```

## 5) What business-facing tables look like
### Current/source table (latest per user)
```sql
CREATE OR REPLACE TABLE dim_user_service_tier_current AS
SELECT user_id, service_tier_id
FROM (
  SELECT
      user_id,
      service_tier_id,
      ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY eff_start_date DESC) AS rn
  FROM dim_user_service_tier_hist
  WHERE active_flag = 1
)
WHERE rn = 1;
```

### History/source_history table
`dim_user_service_tier_hist` keeps the full timeline with effective dates and active flag.

## 6) Average time spent in a tier before moving to another tier
```sql
WITH ordered AS (
  SELECT
      user_id,
      service_tier_id,
      event_ts,
      LEAD(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts) AS next_ts,
      LEAD(service_tier_id) OVER (PARTITION BY user_id ORDER BY event_ts) AS next_tier
  FROM (
    SELECT event_ts, user_id, service_tier_id
    FROM user_tier_events
    QUALIFY ROW_NUMBER() OVER (
      PARTITION BY event_ts, user_id, service_tier_id
      ORDER BY event_ts
    ) = 1
  )
),
moves AS (
  SELECT
      user_id,
      service_tier_id,
      DATEDIFF('second', event_ts, next_ts) AS seconds_in_tier
  FROM ordered
  WHERE next_ts IS NOT NULL
    AND next_tier <> service_tier_id
)
SELECT
    service_tier_id,
    AVG(seconds_in_tier) AS avg_seconds_in_tier,
    AVG(seconds_in_tier) / 3600.0 AS avg_hours_in_tier
FROM moves
GROUP BY service_tier_id
ORDER BY service_tier_id;
```

## 7) Multiple CTEs vs subquery joins: performance impact
- In Snowflake, CTEs are mostly a readability/maintainability construct; optimizer often inlines equivalent logic.
- Performance is usually similar for equivalent plans.
- Prefer multiple CTEs for interview clarity and stepwise validation.
- Real performance drivers: micro-partition pruning, clustering, avoiding unnecessary scans/sorts, and incremental processing.
- If a heavy intermediate result is reused many times, materialize it (temporary/transient table) instead of recomputing.
