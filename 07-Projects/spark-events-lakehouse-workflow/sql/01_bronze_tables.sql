-- Iceberg namespaces
CREATE NAMESPACE IF NOT EXISTS ice.bronze;
CREATE NAMESPACE IF NOT EXISTS ice.silver;
CREATE NAMESPACE IF NOT EXISTS ice.gold;
CREATE NAMESPACE IF NOT EXISTS ice.raw;

-- Bronze raw Kafka envelope
CREATE TABLE IF NOT EXISTS ice.bronze.events_kafka_raw (
  kafka_topic STRING,
  kafka_partition INT,
  kafka_offset BIGINT,
  kafka_timestamp TIMESTAMP,
  ingest_ts TIMESTAMP,
  raw_value STRING
)
USING iceberg
PARTITIONED BY (days(ingest_ts));
