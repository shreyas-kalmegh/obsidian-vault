#!/usr/bin/env bash
set -euo pipefail

# Example only. Replace placeholders before running.

SPARK_BIN="${SPARK_BIN:-spark-submit}"

# Preferred one-time bootstrap from source DB snapshot
$SPARK_BIN \
  --master yarn \
  --deploy-mode cluster \
  --conf spark.sql.adaptive.enabled=true \
  --conf spark.sql.shuffle.partitions=400 \
  --conf spark.executor.instances=8 \
  --conf spark.executor.cores=4 \
  --conf spark.executor.memory=16g \
  --conf spark.sql.catalog.ice=org.apache.iceberg.spark.SparkCatalog \
  --conf spark.sql.catalog.ice.type=hadoop \
  --conf spark.sql.catalog.ice.warehouse=s3://your-bucket/iceberg-warehouse/ \
  --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
  --packages org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.5.2,org.postgresql:postgresql:42.7.3 \
  src/bootstrap_snapshot_from_db.py

# One-time Bronze backfill from Kafka history
$SPARK_BIN \
  --master yarn \
  --deploy-mode cluster \
  --conf spark.sql.adaptive.enabled=true \
  --conf spark.sql.shuffle.partitions=400 \
  --conf spark.executor.instances=8 \
  --conf spark.executor.cores=4 \
  --conf spark.executor.memory=16g \
  --conf spark.sql.catalog.ice=org.apache.iceberg.spark.SparkCatalog \
  --conf spark.sql.catalog.ice.type=hadoop \
  --conf spark.sql.catalog.ice.warehouse=s3://your-bucket/iceberg-warehouse/ \
  --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
  --packages org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.5.2 \
  src/backfill_bronze_from_kafka.py

# Bronze streaming ingestion
$SPARK_BIN \
  --master yarn \
  --deploy-mode cluster \
  --conf spark.sql.adaptive.enabled=true \
  --conf spark.sql.shuffle.partitions=400 \
  --conf spark.executor.instances=8 \
  --conf spark.executor.cores=4 \
  --conf spark.executor.memory=16g \
  --conf spark.sql.catalog.ice=org.apache.iceberg.spark.SparkCatalog \
  --conf spark.sql.catalog.ice.type=hadoop \
  --conf spark.sql.catalog.ice.warehouse=s3://your-bucket/iceberg-warehouse/ \
  --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
  --packages org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.5.2 \
  src/stream_ingest_bronze.py

# SCD2 merge batch job
$SPARK_BIN \
  --master yarn \
  --deploy-mode cluster \
  --conf spark.sql.adaptive.enabled=true \
  --conf spark.sql.shuffle.partitions=300 \
  --conf spark.executor.instances=6 \
  --conf spark.executor.cores=4 \
  --conf spark.executor.memory=16g \
  --conf spark.sql.catalog.ice=org.apache.iceberg.spark.SparkCatalog \
  --conf spark.sql.catalog.ice.type=hadoop \
  --conf spark.sql.catalog.ice.warehouse=s3://your-bucket/iceberg-warehouse/ \
  --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
  --packages org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.5.2 \
  src/scd2_merge_job.py
