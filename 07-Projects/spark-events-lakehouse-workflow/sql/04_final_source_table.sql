CREATE TABLE IF NOT EXISTS ice.raw.events (
  event_id STRING,
  user_id STRING,
  device_id STRING,
  event_type STRING,
  event_ts TIMESTAMP,
  source_created_ts TIMESTAMP,
  source_changed_ts TIMESTAMP,
  op STRING,
  is_deleted BOOLEAN,
  ingest_ts TIMESTAMP,
  source_system STRING,
  source_file STRING,
  payload_hash STRING
)
USING iceberg
PARTITIONED BY (days(event_ts));

MERGE INTO ice.raw.events t
USING (
  SELECT
    event_id,
    user_id,
    device_id,
    event_type,
    event_ts,
    source_created_ts,
    source_changed_ts,
    op,
    is_deleted,
    ingest_ts,
    source_system,
    source_file,
    payload_hash
  FROM ice.silver.events_canonical
  WHERE ingest_ts >= current_timestamp() - INTERVAL 2 HOURS
) s
ON t.event_id = s.event_id
WHEN MATCHED THEN UPDATE SET
  t.user_id = s.user_id,
  t.device_id = s.device_id,
  t.event_type = s.event_type,
  t.event_ts = s.event_ts,
  t.source_created_ts = s.source_created_ts,
  t.source_changed_ts = s.source_changed_ts,
  t.op = s.op,
  t.is_deleted = s.is_deleted,
  t.ingest_ts = s.ingest_ts,
  t.source_system = s.source_system,
  t.source_file = s.source_file,
  t.payload_hash = s.payload_hash
WHEN NOT MATCHED THEN INSERT (
  event_id, user_id, device_id, event_type, event_ts, source_created_ts, source_changed_ts, op, is_deleted, ingest_ts, source_system, source_file, payload_hash
) VALUES (
  s.event_id, s.user_id, s.device_id, s.event_type, s.event_ts, s.source_created_ts, s.source_changed_ts, s.op, s.is_deleted, s.ingest_ts, s.source_system, s.source_file, s.payload_hash
);
