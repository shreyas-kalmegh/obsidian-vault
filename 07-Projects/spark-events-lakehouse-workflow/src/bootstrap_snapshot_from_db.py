from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, lit, sha2, concat_ws


ICEBERG_WAREHOUSE = "s3://your-bucket/iceberg-warehouse/"
TARGET_SILVER_TABLE = "ice.silver.events_canonical"

# JDBC placeholders
JDBC_URL = "jdbc:postgresql://your-read-replica:5432/appdb"
JDBC_USER = "readonly_user"
JDBC_PASSWORD = "readonly_password"
JDBC_DRIVER = "org.postgresql.Driver"

# Replace with a snapshot-compatible query from source DB.
SNAPSHOT_QUERY = """
(
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
    source_system
  FROM events
) AS src
"""


def main() -> None:
    spark = (
        SparkSession.builder.appName("bootstrap-snapshot-from-db")
        .config("spark.sql.catalog.ice", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.ice.type", "hadoop")
        .config("spark.sql.catalog.ice.warehouse", ICEBERG_WAREHOUSE)
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .getOrCreate()
    )

    snapshot_df = (
        spark.read.format("jdbc")
        .option("url", JDBC_URL)
        .option("dbtable", SNAPSHOT_QUERY)
        .option("user", JDBC_USER)
        .option("password", JDBC_PASSWORD)
        .option("driver", JDBC_DRIVER)
        .load()
    )

    staged = (
        snapshot_df.select(
            col("event_id").cast("string").alias("event_id"),
            col("user_id").cast("string").alias("user_id"),
            col("device_id").cast("string").alias("device_id"),
            col("event_type").cast("string").alias("event_type"),
            col("event_ts").cast("timestamp").alias("event_ts"),
            col("source_created_ts").cast("timestamp").alias("source_created_ts"),
            col("source_changed_ts").cast("timestamp").alias("source_changed_ts"),
            col("op").cast("string").alias("op"),
            col("is_deleted").cast("boolean").alias("is_deleted"),
            current_timestamp().alias("ingest_ts"),
            col("source_system").cast("string").alias("source_system"),
            lit("db_snapshot").alias("source_file"),
        )
        .withColumn(
            "payload_hash",
            sha2(
                concat_ws(
                    "||",
                    col("event_id"),
                    col("user_id"),
                    col("device_id"),
                    col("event_type"),
                    col("source_changed_ts").cast("string"),
                ),
                256,
            ),
        )
        .filter(col("event_id").isNotNull() & col("user_id").isNotNull() & col("event_ts").isNotNull())
    )

    staged.createOrReplaceTempView("staged_snapshot_events")

    spark.sql(
        f"""
        MERGE INTO {TARGET_SILVER_TABLE} t
        USING (
          SELECT *
          FROM (
            SELECT
              *,
              row_number() OVER (
                PARTITION BY event_id
                ORDER BY source_changed_ts DESC, ingest_ts DESC
              ) AS rn
            FROM staged_snapshot_events
          ) x
          WHERE rn = 1
        ) s
          ON t.event_id = s.event_id
        WHEN MATCHED AND s.source_changed_ts >= t.source_changed_ts THEN UPDATE SET
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
        )
        """
    )


if __name__ == "__main__":
    main()
