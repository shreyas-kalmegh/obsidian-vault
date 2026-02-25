CREATE TABLE IF NOT EXISTS ice.gold.user_event_profile_scd2 (
  user_id STRING,
  device_id STRING,
  event_type STRING,
  source_created_ts TIMESTAMP,
  source_changed_ts TIMESTAMP,
  valid_from TIMESTAMP,
  valid_to TIMESTAMP,
  is_current BOOLEAN,
  record_hash STRING,
  updated_at TIMESTAMP
)
USING iceberg
PARTITIONED BY (days(valid_from));

-- Invariant check query (run periodically):
-- ensure only one current record per user_id
-- SELECT user_id, count(*) c
-- FROM ice.gold.user_event_profile_scd2
-- WHERE is_current = true
-- GROUP BY user_id
-- HAVING c > 1;
