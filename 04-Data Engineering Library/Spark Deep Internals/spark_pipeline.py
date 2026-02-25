"""
Comprehensive PySpark pipeline that demonstrates high-ROI interview patterns in one flow.

Coverage in this single pipeline:
- S3 read/write patterns
- Iceberg catalog + table writes
- Early filter/projection
- Dedup with window functions
- Null handling and schema normalization
- Left-semi / left-anti joins for existence and quarantine flows
- Broadcast join for small dimensions
- Sessionization pattern with window + cumulative sum
- Top-N per group window ranking
- Skew mitigation via key salting (for heavy-key aggregations)
- Repartition/coalesce and caching decisions
- Data quality metrics and audit columns
"""

from pyspark.sql import SparkSession, DataFrame, Window
from pyspark.sql import functions as F
from pyspark.storagelevel import StorageLevel


# S3 locations (replace with real buckets/prefixes)
S3_RAW_EVENTS = "s3://my-raw-bucket/events/date=*/*.parquet"
S3_RAW_ORDERS = "s3://my-raw-bucket/orders/date=*/*.parquet"
S3_DIM_USERS = "s3://my-curated-bucket/dim/users/*.parquet"
S3_DIM_PRODUCTS = "s3://my-curated-bucket/dim/products/*.parquet"
S3_BLACKLISTED_USERS = "s3://my-control-bucket/security/blacklisted_users/*.csv"
S3_WAREHOUSE = "s3://my-warehouse-bucket/iceberg/"

CATALOG = "ice"


def build_spark() -> SparkSession:
    # Why: configure Iceberg + AQE up front so the job uses the intended runtime behavior.
    spark = (
        SparkSession.builder.appName("spark-interview-pipeline")
        .config(f"spark.sql.catalog.{CATALOG}", "org.apache.iceberg.spark.SparkCatalog")
        .config(f"spark.sql.catalog.{CATALOG}.type", "hadoop")
        .config(f"spark.sql.catalog.{CATALOG}.warehouse", S3_WAREHOUSE)
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.skewJoin.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .config("spark.sql.shuffle.partitions", "400")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
    return spark


def standardize_events(events: DataFrame) -> DataFrame:
    # Why: narrow and clean early to reduce shuffle volume later.
    return (
        events.select(
            F.col("event_id").cast("string"),
            F.col("user_id").cast("string"),
            F.col("device_id").cast("string"),
            F.col("event_type").cast("string"),
            F.to_timestamp("event_ts").alias("event_ts"),
            F.to_date("event_ts").alias("event_date"),
            F.col("ingest_ts").cast("timestamp"),
            F.col("source_file").cast("string"),
        )
        .filter(F.col("user_id").isNotNull() & F.col("event_ts").isNotNull())
    )


def deduplicate_events(events: DataFrame) -> DataFrame:
    # Why: remove duplicate deliveries; keep latest by ingest timestamp.
    w = Window.partitionBy("event_id").orderBy(F.col("ingest_ts").desc_nulls_last())
    return (
        events.withColumn("rn", F.row_number().over(w))
        .filter(F.col("rn") == 1)
        .drop("rn")
    )


def build_sessions(events: DataFrame) -> DataFrame:
    # Sessionization pattern: start a new session if gap > 30 mins.
    w = Window.partitionBy("user_id").orderBy("event_ts")
    gap_minutes = (
        F.unix_timestamp("event_ts") - F.unix_timestamp(F.lag("event_ts").over(w))
    ) / F.lit(60)

    events_with_flags = (
        events.withColumn("gap_minutes", gap_minutes)
        .withColumn(
            "new_session_flag",
            F.when(F.col("gap_minutes").isNull() | (F.col("gap_minutes") > 30), F.lit(1)).otherwise(F.lit(0)),
        )
    )

    session_w = Window.partitionBy("user_id").orderBy("event_ts").rowsBetween(Window.unboundedPreceding, 0)

    return (
        events_with_flags.withColumn("session_num", F.sum("new_session_flag").over(session_w))
        .withColumn("session_id", F.concat_ws("-", F.col("user_id"), F.col("session_num")))
        .drop("gap_minutes", "new_session_flag", "session_num")
    )


def join_and_enrich(events: DataFrame, orders: DataFrame, users: DataFrame, products: DataFrame) -> DataFrame:
    # Why: small dimensions are broadcast to avoid large shuffle join.
    users_small = users.select("user_id", "country", "is_active", "user_tier")
    products_small = products.select("product_id", "category", "brand")

    orders_std = (
        orders.select(
            F.col("order_id").cast("string"),
            F.col("user_id").cast("string"),
            F.col("product_id").cast("string"),
            F.to_timestamp("order_ts").alias("order_ts"),
            F.to_date("order_ts").alias("order_date"),
            F.col("price").cast("double"),
            F.col("quantity").cast("int"),
            F.col("order_status").cast("string"),
        )
        .filter(F.col("order_ts").isNotNull() & F.col("user_id").isNotNull())
        .withColumn("quantity", F.coalesce(F.col("quantity"), F.lit(1)))
        .withColumn("gross_amount", (F.col("price") * F.col("quantity")).cast("double"))
    )

    # left-semi: keep only active users (existence check, no duplicate dim columns)
    active_users = users_small.filter(F.col("is_active") == F.lit(True)).select("user_id").distinct()
    orders_active = orders_std.join(active_users, "user_id", "left_semi")

    # Enrichment joins
    enriched = (
        orders_active.join(F.broadcast(users_small), "user_id", "left")
        .join(F.broadcast(products_small), "product_id", "left")
    )

    # Keep one session per user/day to avoid row multiplication during join.
    session_pick_w = Window.partitionBy("user_id", "event_date").orderBy(F.col("event_ts").desc())
    events_sessions = (
        events.withColumn("rn", F.row_number().over(session_pick_w))
        .filter(F.col("rn") == 1)
        .select("user_id", "event_date", "session_id")
    )

    enriched = (
        enriched.join(
            events_sessions,
            (enriched.user_id == events_sessions.user_id)
            & (enriched.order_date == events_sessions.event_date),
            "left",
        )
        .drop(events_sessions.user_id)
        .drop(events_sessions.event_date)
    )

    return enriched


def quarantine_bad_records(orders: DataFrame, blacklisted: DataFrame) -> DataFrame:
    # left-semi: keep only blocked-user records for quarantine sink.
    return orders.join(blacklisted.select("user_id").distinct(), "user_id", "left_semi")


def skew_safe_daily_agg(enriched: DataFrame) -> DataFrame:
    # Why: heavy keys (e.g., few very large countries) create skew in groupBy.
    # Two-phase salted aggregation reduces single-task hotspots.
    salted = enriched.withColumn("salt", (F.rand() * 16).cast("int"))

    phase1 = (
        salted.groupBy("order_date", "country", "salt")
        .agg(
            F.sum("gross_amount").alias("revenue_part"),
            F.countDistinct("order_id").alias("orders_part"),
            F.approx_count_distinct("user_id").alias("buyers_part"),
        )
    )

    phase2 = (
        phase1.groupBy("order_date", "country")
        .agg(
            F.sum("revenue_part").alias("revenue"),
            F.sum("orders_part").alias("orders"),
            F.sum("buyers_part").alias("buyers_approx"),
        )
    )

    return phase2


def top_products(enriched: DataFrame) -> DataFrame:
    # Top-N per group pattern via window rank.
    w = Window.partitionBy("order_date", "category").orderBy(F.col("revenue").desc(), F.col("product_id"))

    product_daily = (
        enriched.groupBy("order_date", "category", "product_id", "brand")
        .agg(
            F.sum("gross_amount").alias("revenue"),
            F.countDistinct("order_id").alias("orders"),
        )
    )

    return (
        product_daily.withColumn("rn", F.row_number().over(w))
        .filter(F.col("rn") <= 5)
        .drop("rn")
    )


def write_iceberg(df: DataFrame, table: str, mode: str = "overwrite") -> None:
    # Why: writing to Iceberg keeps schema evolution/time travel/table management features.
    if mode == "overwrite":
        df.writeTo(table).using("iceberg").createOrReplace()
    elif mode == "append":
        df.writeTo(table).append()
    else:
        raise ValueError(f"Unsupported mode: {mode}")


def run_pipeline() -> None:
    spark = build_spark()
    spark.sql(f"CREATE NAMESPACE IF NOT EXISTS {CATALOG}.analytics")

    # Read sources from S3
    events_raw = spark.read.parquet(S3_RAW_EVENTS)
    orders_raw = spark.read.parquet(S3_RAW_ORDERS)
    users_dim = spark.read.parquet(S3_DIM_USERS)
    products_dim = spark.read.parquet(S3_DIM_PRODUCTS)
    blacklisted_users = (
        spark.read.option("header", "true").csv(S3_BLACKLISTED_USERS)
        .select(F.col("user_id").cast("string"))
        .filter(F.col("user_id").isNotNull())
    )

    events = deduplicate_events(standardize_events(events_raw)).persist(StorageLevel.MEMORY_AND_DISK)
    events.count()  # materialize cache once; reused downstream

    sessions = build_sessions(events)
    enriched_orders = join_and_enrich(sessions, orders_raw, users_dim, products_dim)

    bad_records = quarantine_bad_records(enriched_orders, blacklisted_users).withColumn(
        "quarantine_reason", F.lit("blacklisted_user")
    )

    # keep only non-blacklisted for analytics outputs
    good_orders = enriched_orders.join(blacklisted_users, "user_id", "left_anti")

    daily_metrics = skew_safe_daily_agg(good_orders).withColumn("etl_ts", F.current_timestamp())
    top5_products = top_products(good_orders).withColumn("etl_ts", F.current_timestamp())

    # Control partitioning before writes
    daily_metrics = daily_metrics.repartition("order_date")
    top5_products = top5_products.repartition("order_date")
    bad_records = bad_records.coalesce(50)

    # Iceberg destinations
    write_iceberg(daily_metrics, f"{CATALOG}.analytics.daily_country_metrics", mode="overwrite")
    write_iceberg(top5_products, f"{CATALOG}.analytics.top5_products_by_category", mode="overwrite")
    write_iceberg(bad_records, f"{CATALOG}.analytics.quarantine_orders", mode="overwrite")

    # Optional SQL metric for quick validation
    spark.sql(
        f"""
        SELECT order_date, SUM(revenue) AS total_revenue
        FROM {CATALOG}.analytics.daily_country_metrics
        GROUP BY order_date
        ORDER BY order_date DESC
        LIMIT 10
        """
    ).show(truncate=False)

    events.unpersist()
    spark.stop()


if __name__ == "__main__":
    run_pipeline()
