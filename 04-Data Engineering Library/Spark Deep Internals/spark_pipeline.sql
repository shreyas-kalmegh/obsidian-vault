-- Spark SQL equivalent (or near-equivalent) for spark_pipeline.py
-- Assumes Spark session is configured with Iceberg catalog 'ice' and S3 warehouse.
--
-- ----------------------------------------------------------------------------
-- WHAT THIS PIPELINE DOES (END-TO-END)
-- ----------------------------------------------------------------------------
-- 1) Reads raw event + order data and dimension/control tables.
-- 2) Standardizes types and removes invalid/null-key records.
-- 3) Deduplicates events by event_id (keeps latest ingest_ts).
-- 4) Builds user sessions with 30-minute inactivity gaps.
-- 5) Filters to active users only (left-semi join).
-- 6) Enriches orders with user/product attributes and same-day session_id.
-- 7) Splits records into:
--      - quarantine_orders (blacklisted users),
--      - good_orders (non-blacklisted users).
-- 8) Computes skew-safe daily country metrics via salted 2-phase aggregation.
-- 9) Computes top-5 products per day/category using window ranking.
-- 10) Writes final outputs to Iceberg analytics tables.
--
-- ----------------------------------------------------------------------------
-- EXPECTED TABLE STRUCTURES
-- ----------------------------------------------------------------------------
-- INPUT: raw.events
--   event_id STRING
--   user_id STRING
--   device_id STRING
--   event_type STRING
--   event_ts TIMESTAMP
--   ingest_ts TIMESTAMP
--   source_file STRING
--
-- INPUT: raw.orders
--   order_id STRING
--   user_id STRING
--   product_id STRING
--   order_ts TIMESTAMP
--   price DOUBLE
--   quantity INT
--   order_status STRING
--
-- INPUT: dim.users
--   user_id STRING
--   country STRING
--   is_active BOOLEAN
--   user_tier STRING
--
-- INPUT: dim.products
--   product_id STRING
--   category STRING
--   brand STRING
--
-- INPUT: control.blacklisted_users
--   user_id STRING
--
-- OUTPUT: ice.analytics.daily_country_metrics
--   order_date DATE
--   country STRING
--   revenue DOUBLE
--   orders BIGINT
--   buyers_approx BIGINT
--   etl_ts TIMESTAMP
--
-- OUTPUT: ice.analytics.top5_products_by_category
--   order_date DATE
--   category STRING
--   product_id STRING
--   brand STRING
--   revenue DOUBLE
--   orders BIGINT
--   etl_ts TIMESTAMP
--
-- OUTPUT: ice.analytics.quarantine_orders
--   All columns from enriched_orders + quarantine_reason STRING
--   (schema is inherited from the enriched projection)

-- Example setup (run once per session if needed):
-- SET spark.sql.catalog.ice = org.apache.iceberg.spark.SparkCatalog;
-- SET spark.sql.catalog.ice.type = hadoop;
-- SET spark.sql.catalog.ice.warehouse = s3://my-warehouse-bucket/iceberg/;
-- SET spark.sql.extensions = org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions;
-- SET spark.sql.adaptive.enabled = true;
-- SET spark.sql.adaptive.skewJoin.enabled = true;
-- SET spark.sql.shuffle.partitions = 400;

-- ---------------------------------------------------------------------------
-- 1) Source tables/views (replace with your actual external tables)
-- ---------------------------------------------------------------------------
-- raw.events(event_id, user_id, device_id, event_type, event_ts, ingest_ts, source_file)
-- raw.orders(order_id, user_id, product_id, order_ts, price, quantity, order_status)
-- dim.users(user_id, country, is_active, user_tier)
-- dim.products(product_id, category, brand)
-- control.blacklisted_users(user_id)

-- ---------------------------------------------------------------------------
-- 2) Normalize + deduplicate events
-- ---------------------------------------------------------------------------
WITH events_std AS (
    SELECT
        CAST(event_id AS STRING) AS event_id,
        CAST(user_id AS STRING) AS user_id,
        CAST(device_id AS STRING) AS device_id,
        CAST(event_type AS STRING) AS event_type,
        CAST(event_ts AS TIMESTAMP) AS event_ts,
        TO_DATE(event_ts) AS event_date,
        CAST(ingest_ts AS TIMESTAMP) AS ingest_ts,
        CAST(source_file AS STRING) AS source_file
    FROM raw.events
    WHERE user_id IS NOT NULL
      AND event_ts IS NOT NULL
),
events_dedup AS (
    SELECT *
    FROM (
        SELECT
            e.*,
            ROW_NUMBER() OVER (
                PARTITION BY e.event_id
                ORDER BY e.ingest_ts DESC
            ) AS rn
        FROM events_std e
    ) x
    WHERE rn = 1
),

-- ---------------------------------------------------------------------------
-- 3) Sessionization (30-minute inactivity threshold)
-- ---------------------------------------------------------------------------
events_flagged AS (
    SELECT
        e.*,
        (UNIX_TIMESTAMP(event_ts)
         - UNIX_TIMESTAMP(LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts))) / 60.0 AS gap_minutes
    FROM events_dedup e
),
events_sessions AS (
    SELECT
        ef.*,
        CONCAT(
            ef.user_id,
            '-',
            SUM(CASE WHEN ef.gap_minutes IS NULL OR ef.gap_minutes > 30 THEN 1 ELSE 0 END)
                OVER (
                    PARTITION BY ef.user_id
                    ORDER BY ef.event_ts
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )
        ) AS session_id
    FROM events_flagged ef
),
events_sessions_latest_day AS (
    SELECT user_id, event_date, session_id
    FROM (
        SELECT
            es.user_id,
            es.event_date,
            es.session_id,
            ROW_NUMBER() OVER (
                PARTITION BY es.user_id, es.event_date
                ORDER BY es.event_ts DESC
            ) AS rn
        FROM events_sessions es
    ) x
    WHERE rn = 1
),

-- ---------------------------------------------------------------------------
-- 4) Orders normalization + active-user semi join
-- ---------------------------------------------------------------------------
orders_std AS (
    SELECT
        CAST(order_id AS STRING) AS order_id,
        CAST(user_id AS STRING) AS user_id,
        CAST(product_id AS STRING) AS product_id,
        CAST(order_ts AS TIMESTAMP) AS order_ts,
        TO_DATE(order_ts) AS order_date,
        CAST(price AS DOUBLE) AS price,
        COALESCE(CAST(quantity AS INT), 1) AS quantity,
        CAST(order_status AS STRING) AS order_status,
        CAST(price AS DOUBLE) * COALESCE(CAST(quantity AS INT), 1) AS gross_amount
    FROM raw.orders
    WHERE order_ts IS NOT NULL
      AND user_id IS NOT NULL
),
active_orders AS (
    SELECT o.*
    FROM orders_std o
    LEFT SEMI JOIN (
        SELECT DISTINCT user_id
        FROM dim.users
        WHERE is_active = TRUE
    ) au
    ON o.user_id = CAST(au.user_id AS STRING)
),

-- ---------------------------------------------------------------------------
-- 5) Enrichment joins (broadcast hints where dims are small)
-- ---------------------------------------------------------------------------
enriched_orders AS (
    SELECT
        o.*,
        u.country,
        u.user_tier,
        p.category,
        p.brand,
        s.session_id
    FROM active_orders o
    LEFT JOIN /*+ BROADCAST(u) */ dim.users u
      ON o.user_id = CAST(u.user_id AS STRING)
    LEFT JOIN /*+ BROADCAST(p) */ dim.products p
      ON o.product_id = CAST(p.product_id AS STRING)
    LEFT JOIN (
        SELECT user_id, event_date, session_id
        FROM events_sessions_latest_day
    ) s
      ON o.user_id = s.user_id
     AND o.order_date = s.event_date
),

-- ---------------------------------------------------------------------------
-- 6) Quarantine and good orders split
-- ---------------------------------------------------------------------------
quarantine_orders AS (
    SELECT
        e.*,
        'blacklisted_user' AS quarantine_reason
    FROM enriched_orders e
    LEFT SEMI JOIN control.blacklisted_users b
      ON e.user_id = CAST(b.user_id AS STRING)
),
good_orders AS (
    SELECT e.*
    FROM enriched_orders e
    LEFT ANTI JOIN control.blacklisted_users b
      ON e.user_id = CAST(b.user_id AS STRING)
),

-- ---------------------------------------------------------------------------
-- 7) Skew-safe daily country metrics (salted two-phase aggregation)
-- ---------------------------------------------------------------------------
salted AS (
    SELECT
        g.*,
        CAST(RAND() * 16 AS INT) AS salt
    FROM good_orders g
),
daily_phase1 AS (
    SELECT
        order_date,
        country,
        salt,
        SUM(gross_amount) AS revenue_part,
        COUNT(DISTINCT order_id) AS orders_part,
        APPROX_COUNT_DISTINCT(user_id) AS buyers_part
    FROM salted
    GROUP BY order_date, country, salt
),
daily_country_metrics AS (
    SELECT
        order_date,
        country,
        SUM(revenue_part) AS revenue,
        SUM(orders_part) AS orders,
        SUM(buyers_part) AS buyers_approx,
        CURRENT_TIMESTAMP() AS etl_ts
    FROM daily_phase1
    GROUP BY order_date, country
),

-- ---------------------------------------------------------------------------
-- 8) Top-5 products per day/category
-- ---------------------------------------------------------------------------
product_daily AS (
    SELECT
        order_date,
        category,
        product_id,
        brand,
        SUM(gross_amount) AS revenue,
        COUNT(DISTINCT order_id) AS orders
    FROM good_orders
    GROUP BY order_date, category, product_id, brand
),
top5_products_by_category AS (
    SELECT *
    FROM (
        SELECT
            p.*,
            ROW_NUMBER() OVER (
                PARTITION BY p.order_date, p.category
                ORDER BY p.revenue DESC, p.product_id ASC
            ) AS rn
        FROM product_daily p
    ) x
    WHERE rn <= 5
)

-- ---------------------------------------------------------------------------
-- 9) Writes to Iceberg tables
-- ---------------------------------------------------------------------------
-- Use CTAS/REPLACE TABLE style for overwrite semantics.

CREATE OR REPLACE TABLE ice.analytics.daily_country_metrics
USING iceberg
PARTITIONED BY (order_date)
AS
SELECT * FROM daily_country_metrics;

CREATE OR REPLACE TABLE ice.analytics.top5_products_by_category
USING iceberg
PARTITIONED BY (order_date)
AS
SELECT
    order_date,
    category,
    product_id,
    brand,
    revenue,
    orders,
    CURRENT_TIMESTAMP() AS etl_ts
FROM top5_products_by_category;

CREATE OR REPLACE TABLE ice.analytics.quarantine_orders
USING iceberg
AS
SELECT * FROM quarantine_orders;

-- ---------------------------------------------------------------------------
-- 10) Validation query
-- ---------------------------------------------------------------------------
SELECT
    order_date,
    SUM(revenue) AS total_revenue
FROM ice.analytics.daily_country_metrics
GROUP BY order_date
ORDER BY order_date DESC
LIMIT 10;
