# Architecture
- Capture: Debezium -> Kafka
- Stream processing: Flink (for exactly-once) or Spark Structured Streaming
- Storage: Iceberg on S3
- Catalog: Glue / Hive Metastore
- Downstream: Presto/Trino for analytics

Notes:
- Design compaction/retention strategies for the lakehouse.
