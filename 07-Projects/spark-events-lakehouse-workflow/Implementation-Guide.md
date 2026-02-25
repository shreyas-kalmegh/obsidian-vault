# Implementation Guide

## 1. Prerequisites
- Spark 3.3+ (3.4+ preferred)
- Iceberg runtime + Spark SQL Iceberg extensions
- Kafka bootstrap access + topic `events`
- S3 bucket paths for data and checkpoints
- Iceberg catalog configured (example: `ice`)

## 2. Data Contract (Example)

Incoming Kafka value JSON (example):

```json
{
  "event_id": "9ec1d8e7-...",
  "user_id": "cust_123",
  "device_id": "ios-a1",
  "event_type": "profile_updated",
  "event_ts": "2026-02-25T11:21:33Z",
  "source_created_ts": "2026-02-25T11:21:33Z",
  "source_changed_ts": "2026-02-25T11:25:09Z",
  "op": "U",
  "is_deleted": false,
  "source_system": "mobile_app"
}
```

Required:
- `event_id`
- `user_id`
- `event_type`
- `event_ts`
- `source_created_ts`
- `source_changed_ts`

## 3. Run Order
1. Execute `sql/01_bronze_tables.sql`
2. Run `src/bootstrap_snapshot_from_db.py` (preferred one-time historical bootstrap)
3. Start `src/stream_ingest_bronze.py` (continuous CDC/events ingestion)
4. Execute `sql/02_silver_events.sql` (scheduled)
5. Execute `sql/03_scd2_table.sql` once (table create)
6. Run `src/scd2_merge_job.py` (scheduled; Gold SCD2)
7. Execute `sql/04_final_source_table.sql` (scheduled or incremental merge)

## 4. Backfill and Cutover Procedure (Avoiding Duplicates)
If Kafka retention does not cover full history, use the snapshot+CDC playbook below instead of Kafka-only backfill.

### 4A. Preferred: Snapshot + CDC Cutover

1. Take consistent snapshot:
- Run `src/bootstrap_snapshot_from_db.py` against read replica at a known high watermark (`source_changed_ts`).

2. Start streaming ingestion:
- Start `src/stream_ingest_bronze.py`.
- Process Bronze -> Silver continuously/scheduled.

3. Overlap handling:
- Keep overlap window between snapshot watermark and stream start.
- In Silver `MERGE`, latest `source_changed_ts` wins for same `event_id`.

4. Cutover validation:
- No duplicate `event_id` in Silver.
- Freshness lag within SLA (`ingest_ts - source_changed_ts`).
- Source count parity checks for sampled time ranges.

### 4B. Fallback: Kafka-Only Backfill
Use this only when required history is inside Kafka retention window.

1. Pick cutover offsets:
- Capture a fixed `KAFKA_ENDING_OFFSETS` JSON for backfill.
- Example: `{"events":{"0":12345,"1":99887}}`

2. Backfill Bronze:
- In `src/backfill_bronze_from_kafka.py`, set:
  - `KAFKA_STARTING_OFFSETS="earliest"`
  - `KAFKA_ENDING_OFFSETS=<fixed cutover offsets>`
- Run the job once.

3. Start live streaming:
- Start `src/stream_ingest_bronze.py` with:
  - `KAFKA_STARTING_OFFSETS=<same cutover offsets>` for safe overlap, or
  - `latest` after cutover completes

4. Why duplicates are avoided:
- Bronze uses `MERGE` keyed by `(kafka_topic, kafka_partition, kafka_offset)`.
- Reprocessed overlap offsets are ignored.
- Silver and final source remain idempotent via `MERGE` on `event_id`.

5. Validate before enabling downstream schedules:
- `SELECT COUNT(*) FROM ice.bronze.events_kafka_raw`
- Check Bronze uniqueness:
  - `SELECT kafka_topic, kafka_partition, kafka_offset, COUNT(*) c FROM ice.bronze.events_kafka_raw GROUP BY 1,2,3 HAVING c > 1`
- Check Silver event uniqueness:
  - `SELECT event_id, COUNT(*) c FROM ice.silver.events_canonical GROUP BY 1 HAVING c > 1`

## 5. Layering Guidance: Silver vs Gold SCD2
- Silver:
  - Canonical cleaned events, dedup, type normalization, data quality.
  - Do not default to SCD2 in Silver unless many domains require shared historical conformed dimensions.
- Gold:
  - Business models and serving tables.
  - SCD2 belongs here by default (`ice.gold.user_event_profile_scd2`).

## 6. Scheduling Guidance
- Bronze stream: continuous
- Silver transform: every 5-15 minutes
- SCD2 merge: every 15-60 minutes
- Final source refresh: after SCD2 merge

## 7. Operational Checks
- Bronze lag:
  - Compare latest Kafka offsets vs processed offsets
- Silver data quality:
  - Null `user_id`/`event_id` counts
  - Dedup drop rate
  - Latency SLI: `ingest_ts - source_changed_ts`
- SCD2 quality:
  - Only one `is_current = true` per `user_id`
  - No overlapping `valid_from`/`valid_to` ranges
- Final source:
  - Row count drift checks vs Silver

## 8. Cost/Performance Tuning
- Compact small files in Silver/Gold periodically
- Iceberg maintenance: snapshot expiration + manifest rewrite + file compaction
- Tune shuffle partitions relative to cluster size
- Use AQE for skew-heavy joins

## 9. Better Alternatives by Use Case
1. If strict point-in-time analytics is needed:
- Keep event fact table immutable
- Build PIT joins at query time or precompute snapshot tables

2. If updates are very high-frequency:
- Consider Iceberg/Hudi with optimized merge-on-read strategy

3. If exactly-once end-to-end is mandatory:
- Add transactional sink guarantees and stronger idempotency keys
- Avoid relying only on Kafka at-least-once + downstream dedup
