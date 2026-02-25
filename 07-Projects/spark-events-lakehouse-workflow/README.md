# Spark Events Lakehouse Workflow (Iceberg)

End-to-end workflow for:
- Ingesting Kafka `events` stream into S3 data lake
- Producing a canonical `ice.raw.events` source table for the transformation pipeline
- Building Gold SCD Type 2 history from canonical events

## Canonical Source Schema (`ice.raw.events`)

Base contract from transformation pipeline:
- `event_id STRING`
- `user_id STRING`
- `device_id STRING`
- `event_type STRING`
- `event_ts TIMESTAMP`
- `ingest_ts TIMESTAMP`
- `source_file STRING`

Recommended operational extensions:
- `source_created_ts TIMESTAMP`
- `source_changed_ts TIMESTAMP`
- `op STRING`
- `is_deleted BOOLEAN`
- `source_system STRING`
- `payload_hash STRING`

## Directory Layout
```text
07-Projects/spark-events-lakehouse-workflow/
  README.md
  Architecture.md
  Implementation-Guide.md
  sql/
    01_bronze_tables.sql
    02_silver_events.sql
    03_scd2_table.sql
    04_final_source_table.sql
  src/
    stream_ingest_bronze.py
    backfill_bronze_from_kafka.py
    scd2_merge_job.py
  configs/
    spark-submit-example.sh
```

## Data Flow
1. Kafka topic `events` -> `ice.bronze.events_kafka_raw`
2. Bronze parse/dedup -> `ice.silver.events_canonical`
3. Silver -> `ice.gold.user_event_profile_scd2`
4. Silver -> final source table `ice.raw.events`

## Why Iceberg
- Native S3 table management
- Snapshot-based reliability and rollback
- Schema evolution support
- Good interoperability for Spark/Trino/Flink ecosystems

## Better Approach Guidance
Use SCD2 only for mutable entity history requirements.

If your downstream only needs immutable event facts:
- Keep `ice.raw.events` as append/dedup canonical source
- Skip SCD2 for core event processing
- Build SCD2 only for specific dimensions that need historical change tracking

Keep `ingest_ts` even with source timestamps:
- Enables source-to-lake latency monitoring
- Supports replay windows and incident triage
- Provides deterministic tiebreaking for duplicates

## Retention-Safe Bootstrap (Recommended)
Kafka-only backfill works only inside Kafka retention windows.

Preferred bootstrap for production:
1. Load historical snapshot from source DB read replica into Silver (`ice.silver.events_canonical`).
2. Start Kafka CDC ingestion for incremental changes.
3. Run overlap-safe `MERGE` with latest `source_changed_ts` winner.
4. Build Gold SCD2 and final source from Silver.

Template job for snapshot bootstrap:
- `src/bootstrap_snapshot_from_db.py`

## Quick Start
1. Update S3/Kafka/catalog placeholders in `sql/` and `src/` files.
2. Run `sql/01_bronze_tables.sql`.
3. Run one-time `src/backfill_bronze_from_kafka.py` (historical load).
4. Start continuous `src/stream_ingest_bronze.py` after backfill cutover.
5. Run `sql/02_silver_events.sql` on schedule.
6. Run `sql/03_scd2_table.sql` once, then `src/scd2_merge_job.py` on schedule.
7. Run `sql/04_final_source_table.sql` to upsert final `ice.raw.events` source table.

## Backfill + Cutover (No Duplicate Strategy)
Use this only if required history is fully covered by Kafka retention.

1. Freeze a backfill upper bound by choosing `KAFKA_ENDING_OFFSETS` in `backfill_bronze_from_kafka.py`.
2. Run backfill job from `earliest` to that fixed ending offset.
3. Start streaming ingestion with either:
- `KAFKA_STARTING_OFFSETS` equal to the same cutover offsets, or
- `latest` after cutover is complete.
4. Duplicates are prevented at Bronze by `MERGE` on `(kafka_topic, kafka_partition, kafka_offset)`.
5. Silver and final source remain idempotent via `MERGE` on `event_id`.

## Related
- [[04-Data Engineering Library/Spark Deep Internals/spark_pipeline.sql]]
- [[04-Data Engineering Library/Spark Deep Internals/spark_pipeline.py]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Checkpointing.md]]
