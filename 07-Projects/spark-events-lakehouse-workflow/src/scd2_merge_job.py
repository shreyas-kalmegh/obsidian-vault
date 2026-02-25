from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, lit, lead, coalesce, sha2, concat_ws
from pyspark.sql.window import Window


SILVER_TABLE = "ice.silver.events_canonical"
SCD2_TABLE = "ice.gold.user_event_profile_scd2"
ICEBERG_WAREHOUSE = "s3://your-bucket/iceberg-warehouse/"


def build_candidate_versions(spark: SparkSession):
    source = (
        spark.table(SILVER_TABLE)
        .filter(col("user_id").isNotNull())
        .select(
            "user_id",
            "device_id",
            "event_type",
            "source_created_ts",
            "source_changed_ts",
            "event_ts",
            "op",
        )
    )

    w = Window.partitionBy("user_id").orderBy(coalesce(col("source_changed_ts"), col("event_ts")))
    staged = (
        source.withColumn("valid_from", coalesce(col("source_changed_ts"), col("event_ts")))
        .withColumn("next_time", lead(coalesce(col("source_changed_ts"), col("event_ts"))).over(w))
        .withColumn("valid_to", col("next_time"))
        .drop("next_time")
        .withColumn("is_current", lit(False))
        .withColumn(
            "record_hash",
            sha2(concat_ws("||", col("user_id"), col("device_id"), col("event_type")), 256),
        )
    )

    max_time = (
        source.withColumn("effective_time", coalesce(col("source_changed_ts"), col("event_ts")))
        .groupBy("user_id")
        .agg({"effective_time": "max"})
        .withColumnRenamed("max(effective_time)", "max_effective_time")
    )

    staged = (
        staged.join(max_time, on="user_id", how="left")
        .withColumn("is_current", col("valid_from") == col("max_effective_time"))
        .withColumn(
            "valid_to",
            col("valid_to").cast("timestamp"),
        )
        .drop("max_effective_time", "event_ts", "op")
        .withColumn("updated_at", current_timestamp())
        .select(
            "user_id",
            "device_id",
            "event_type",
            "source_created_ts",
            "source_changed_ts",
            "valid_from",
            "valid_to",
            "is_current",
            "record_hash",
            "updated_at",
        )
    )

    return staged


def main() -> None:
    spark = (
        SparkSession.builder.appName("events-scd2-merge-job")
        .config("spark.sql.catalog.ice", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.ice.type", "hadoop")
        .config("spark.sql.catalog.ice.warehouse", ICEBERG_WAREHOUSE)
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .getOrCreate()
    )

    candidates = build_candidate_versions(spark)
    candidates.createOrReplaceTempView("staged_scd2")

    spark.sql(
        f"""
        MERGE INTO {SCD2_TABLE} t
        USING staged_scd2 s
          ON t.user_id = s.user_id
         AND t.valid_from = s.valid_from
        WHEN MATCHED THEN UPDATE SET
          t.device_id = s.device_id,
          t.event_type = s.event_type,
          t.source_created_ts = s.source_created_ts,
          t.source_changed_ts = s.source_changed_ts,
          t.valid_to = s.valid_to,
          t.is_current = s.is_current,
          t.record_hash = s.record_hash,
          t.updated_at = s.updated_at
        WHEN NOT MATCHED THEN INSERT (
          user_id, device_id, event_type, source_created_ts, source_changed_ts, valid_from, valid_to, is_current, record_hash, updated_at
        ) VALUES (
          s.user_id, s.device_id, s.event_type, s.source_created_ts, s.source_changed_ts, s.valid_from, s.valid_to, s.is_current, s.record_hash, s.updated_at
        )
        """
    )


if __name__ == "__main__":
    main()
