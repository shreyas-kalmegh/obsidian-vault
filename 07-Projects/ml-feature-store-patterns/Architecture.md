# Architecture
- Offline store: Parquet/Iceberg
- Online store: Redis or DynamoDB
- Ingestion: Streaming pipelines to update online store

Notes:
- Include schema evolution and rollback strategies.
