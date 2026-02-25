# CDC and Incremental Modeling

## Overview
CDC (Change Data Capture) propagates inserts, updates, and deletes from source systems.
Incremental modeling applies only changed data, avoiding full reloads.

## Core Concepts
- Change key: business key identifying entity (`customer_id`, `order_id`)
- Change order: source change timestamp, version, or log position
- Idempotency: reprocessing same batch should not duplicate outcomes

## Typical Merge Pattern
Use business key plus latest change ordering column:

```sql
MERGE INTO silver.customer t
USING staged_changes s
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.source_changed_ts >= t.source_changed_ts THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...;
```

## Delete Semantics
Choose explicitly:
- Soft delete: keep row with `is_deleted = true`
- Hard delete: remove row
- Tombstone + downstream policy

## Incremental Watermark Strategies
- Source timestamp watermark (`source_changed_ts > last_success_ts`)
- Log position watermark (LSN/SCN/binlog offset)
- Partition + high watermark combination

Prefer source log position where available for correctness.

## Example: Customer Profile CDC
- Bronze captures raw CDC events
- Silver keeps latest profile by `customer_id`
- Gold Type 2 dimension keeps attribute history for reporting

## Recovery and Reprocessing
- Keep deterministic staging windows
- Store job metadata (`batch_id`, watermark, row counts)
- Provide replay path from Bronze for incident correction

## Common Mistakes
- Using `ingest_ts` as business truth ordering
- Ignoring late or out-of-order updates
- No strategy for schema evolution in CDC payloads

## Practical Checklist
1. Define idempotency key and ordering column.
2. Define delete handling semantics.
3. Track watermark per pipeline.
4. Test re-run and backfill behavior.

## Related Notes
- [[late-arriving-data]]
- [[scd-types]]
