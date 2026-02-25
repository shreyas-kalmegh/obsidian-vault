CREATE TABLE IF NOT EXISTS ice.silver.events_canonical (
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

-- Incremental upsert from Bronze to Silver.
MERGE INTO ice.silver.events_canonical t
USING (
  WITH parsed AS (
    SELECT
      from_json(
        raw_value,
        'event_id string, user_id string, device_id string, event_type string, event_ts string, source_created_ts string, source_changed_ts string, op string, is_deleted boolean, source_system string'
      ) AS j,
      raw_value,
      ingest_ts,
      kafka_topic,
      kafka_partition,
      kafka_offset
    FROM ice.bronze.events_kafka_raw
    WHERE ingest_ts >= current_timestamp() - INTERVAL 2 HOURS
  ),
  normalized AS (
    SELECT
      j.event_id AS event_id,
      j.user_id AS user_id,
      j.device_id AS device_id,
      j.event_type AS event_type,
      to_timestamp(j.event_ts) AS event_ts,
      coalesce(to_timestamp(j.source_created_ts), to_timestamp(j.event_ts)) AS source_created_ts,
      greatest(
        coalesce(to_timestamp(j.source_changed_ts), to_timestamp(j.event_ts)),
        coalesce(to_timestamp(j.source_created_ts), to_timestamp(j.event_ts))
      ) AS source_changed_ts,
      coalesce(j.op, 'U') AS op,
      coalesce(j.is_deleted, false) AS is_deleted,
      ingest_ts,
      coalesce(j.source_system, 'unknown') AS source_system,
      concat(kafka_topic, ':', cast(kafka_partition as string), ':', cast(kafka_offset as string)) AS source_file,
      sha2(raw_value, 256) AS payload_hash
    FROM parsed
    WHERE j.event_id IS NOT NULL
      AND j.user_id IS NOT NULL
      AND to_timestamp(j.event_ts) IS NOT NULL
  )
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
  FROM (
    SELECT
      *,
      row_number() OVER (
        PARTITION BY event_id
        ORDER BY coalesce(source_changed_ts, event_ts) DESC, ingest_ts DESC
      ) AS rn
    FROM normalized
  ) d
  WHERE rn = 1
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
