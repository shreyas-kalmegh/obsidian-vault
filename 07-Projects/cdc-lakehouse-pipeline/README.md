# CDC Lakehouse Pipeline
Purpose: Capture change data (CDC) from OLTP DBs and provide a near-real-time lakehouse using Kafka + Flink/Spark and Iceberg/Delta.

Guidelines:
- Use Debezium or native CDC capture.
- Maintain schema registry for Avro/Protobuf.
- Handle out-of-order events and idempotency.

Architecture.md
