from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, current_timestamp


KAFKA_BOOTSTRAP = "your-kafka-bootstrap:9092"
KAFKA_TOPIC = "events"
KAFKA_STARTING_OFFSETS = "latest"
CHECKPOINT_PATH = "s3://your-bucket/checkpoints/bronze_events_raw"
BRONZE_TABLE = "ice.bronze.events_kafka_raw"
ICEBERG_WAREHOUSE = "s3://your-bucket/iceberg-warehouse/"


def merge_bronze_batch(batch_df: DataFrame, _: int) -> None:
    batch_df.createOrReplaceTempView("staged_bronze_events")
    batch_df.sparkSession.sql(
        f"""
        MERGE INTO {BRONZE_TABLE} t
        USING staged_bronze_events s
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


def main() -> None:
    spark = (
        SparkSession.builder.appName("stream-ingest-bronze-events")
        .config("spark.sql.catalog.ice", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.ice.type", "hadoop")
        .config("spark.sql.catalog.ice.warehouse", ICEBERG_WAREHOUSE)
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .config("spark.sql.streaming.stateStore.providerClass",
                "org.apache.spark.sql.execution.streaming.state.HDFSBackedStateStoreProvider")
        .getOrCreate()
    )

    kafka_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
        .option("subscribe", KAFKA_TOPIC)
        .option("startingOffsets", KAFKA_STARTING_OFFSETS)
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

    query = (
        bronze_df.writeStream
        .outputMode("append")
        .option("checkpointLocation", CHECKPOINT_PATH)
        .foreachBatch(merge_bronze_batch)
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()
