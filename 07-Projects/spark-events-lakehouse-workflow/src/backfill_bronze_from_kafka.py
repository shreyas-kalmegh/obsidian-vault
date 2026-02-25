from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp


KAFKA_BOOTSTRAP = "your-kafka-bootstrap:9092"
KAFKA_TOPIC = "events"
KAFKA_STARTING_OFFSETS = "earliest"
# Set to a fixed offset JSON at cutover time for deterministic replay.
# Example: {"events":{"0":12345,"1":99887}}
KAFKA_ENDING_OFFSETS = "latest"
BRONZE_TABLE = "ice.bronze.events_kafka_raw"
ICEBERG_WAREHOUSE = "s3://your-bucket/iceberg-warehouse/"


def main() -> None:
    spark = (
        SparkSession.builder.appName("backfill-bronze-from-kafka")
        .config("spark.sql.catalog.ice", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.ice.type", "hadoop")
        .config("spark.sql.catalog.ice.warehouse", ICEBERG_WAREHOUSE)
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .getOrCreate()
    )

    kafka_df = (
        spark.read.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
        .option("subscribe", KAFKA_TOPIC)
        .option("startingOffsets", KAFKA_STARTING_OFFSETS)
        .option("endingOffsets", KAFKA_ENDING_OFFSETS)
        .option("failOnDataLoss", "false")
        .load()
    )

    bronze_df = kafka_df.select(
        col("topic").alias("kafka_topic"),
        col("partition").cast("int").alias("kafka_partition"),
        col("offset").cast("bigint").alias("kafka_offset"),
        col("timestamp").alias("kafka_timestamp"),
        current_timestamp().alias("ingest_ts"),
        col("value").cast("string").alias("raw_value"),
    )

    bronze_df.createOrReplaceTempView("staged_backfill_bronze_events")

    spark.sql(
        f"""
        MERGE INTO {BRONZE_TABLE} t
        USING staged_backfill_bronze_events s
          ON t.kafka_topic = s.kafka_topic
         AND t.kafka_partition = s.kafka_partition
         AND t.kafka_offset = s.kafka_offset
        WHEN NOT MATCHED THEN INSERT (
          kafka_topic, kafka_partition, kafka_offset, kafka_timestamp, ingest_ts, raw_value
        ) VALUES (
          s.kafka_topic, s.kafka_partition, s.kafka_offset, s.kafka_timestamp, s.ingest_ts, s.raw_value
        )
        """
    )


if __name__ == "__main__":
    main()
