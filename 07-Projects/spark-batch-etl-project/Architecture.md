# Architecture
- Ingest: S3 raw bucket
- Processing: Spark on EMR/Kubernetes
- Storage: S3 curated (partitioned Parquet)
- Orchestration: Airflow or Step Functions
- Monitoring: CloudWatch / Prometheus

Notes:
- Include data validation steps and quality checks.
