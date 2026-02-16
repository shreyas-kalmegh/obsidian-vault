# Architecture
- Source: Kafka topics
- Processing: Flink cluster (Kubernetes)
- State backend: RocksDB + S3 incremental checkpoints
- Sink: Parquet to S3 / Iceberg table
- Orchestration: Kubernetes CronJobs for jobs + CI/CD

Notes:
- Include monitoring for checkpoint durations and backpressure.
