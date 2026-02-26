# Spark Data Modeling: Partitioning and Schema Evolution

This guide focuses on two high-impact design decisions:
- partitioning scheme
- safe schema evolution

## 1) Partitioning Scheme

### 1.1 What partitioning solves
Partitioning reduces scanned data and improves write/read efficiency when queries commonly filter on partition columns.

Good fit:
- frequent predicates like `WHERE event_date = '2026-02-01'`
- large tables with time-based access patterns

Poor fit:
- high-cardinality keys (`user_id`, `session_id`) causing too many small partitions

### 1.2 How to choose partition columns
Use this order:
1. Columns used most in filters
2. Low-to-medium cardinality
3. Stable value distribution (avoid severe skew)

Typical choice:
- `event_date` (daily partition)

Avoid:
- partitioning by raw timestamp or unique identifiers

### 1.3 Recommended partition granularity
- default: daily (`event_date`)
- hourly only if data volume per day is very large and hourly filtering is common
- monthly for smaller datasets where daily would create too many tiny files

### 1.4 SQL examples

Create partitioned table:
```sql
CREATE TABLE analytics.events_fact (
  user_id STRING,
  event_ts TIMESTAMP,
  event_type STRING,
  amount DECIMAL(18,2)
)
USING PARQUET
PARTITIONED BY (event_date DATE);
```

Insert with dynamic partition:
```sql
INSERT INTO analytics.events_fact
SELECT
  user_id,
  event_ts,
  event_type,
  amount,
  TO_DATE(event_ts) AS event_date
FROM staging.events_raw;
```

Read with partition pruning:
```sql
SELECT event_type, COUNT(*)
FROM analytics.events_fact
WHERE event_date BETWEEN DATE '2026-02-01' AND DATE '2026-02-07'
GROUP BY event_type;
```

### 1.5 Target file/partition sizing
Rules of thumb:
- target output file size around `128MB-256MB`
- too many tiny files -> increase compaction/coalesce before write
- very large files with skew/spill -> increase parallelism/repartition before write

Example write shaping:
```sql
INSERT OVERWRITE TABLE analytics.events_fact
SELECT /*+ REPARTITION(200, event_date) */
  user_id,
  event_ts,
  event_type,
  amount,
  TO_DATE(event_ts) AS event_date
FROM staging.events_raw;
```

Then reduce file count in final step when needed:
```sql
SELECT /*+ COALESCE(80) */ *
FROM analytics.events_fact
WHERE event_date = DATE '2026-02-01';
```

## 2) Schema Evolution

### 2.1 Common evolution cases
1. Add nullable column (safest)
2. Reorder columns (logical no-op in SQL)
3. Widen data type (for example `INT -> BIGINT`)
4. Rename/drop columns (riskier; depends on table format)

### 2.2 Safe-first policy
- prefer additive changes first
- backfill new columns explicitly
- avoid destructive changes during peak usage
- test downstream jobs before promoting

### 2.3 Add column example
```sql
ALTER TABLE analytics.events_fact
ADD COLUMNS (source_system STRING);
```

Backfill example:
```sql
INSERT OVERWRITE TABLE analytics.events_fact
SELECT
  user_id,
  event_ts,
  event_type,
  amount,
  event_date,
  COALESCE(source_system, 'unknown') AS source_system
FROM analytics.events_fact;
```

### 2.4 Type evolution example
Safer pattern is create-and-swap for major type changes:
```sql
CREATE TABLE analytics.events_fact_v2 (
  user_id STRING,
  event_ts TIMESTAMP,
  event_type STRING,
  amount DECIMAL(20,4),
  event_date DATE,
  source_system STRING
)
USING PARQUET
PARTITIONED BY (event_date);

INSERT INTO analytics.events_fact_v2
SELECT
  user_id,
  event_ts,
  event_type,
  CAST(amount AS DECIMAL(20,4)) AS amount,
  event_date,
  source_system
FROM analytics.events_fact;
```

### 2.5 Reader-side merge schema (when needed)
If historical files have different schemas, enable schema merging only when required because it adds overhead.

PySpark read example:
```python
spark.read.option("mergeSchema", "true").parquet("/data/events_fact")
```

### 2.6 Write with schema merge (table-format dependent)
For formats like Delta/Iceberg/Hudi, schema evolution support is stronger than plain Parquet tables.

Example (Delta-style in PySpark):
```python
(df.write
   .format("delta")
   .mode("append")
   .option("mergeSchema", "true")
   .saveAsTable("analytics.events_fact"))
```

## 3) Interview-Ready Design Answer
Use this concise structure:
1. Partition by query predicate (`event_date`) and keep partition cardinality controlled.
2. Size partitions/files for stable parallelism (roughly `128MB-256MB` files).
3. Apply additive schema evolution first; use create-and-swap for risky type changes.
4. Use format-native schema evolution (Delta/Iceberg/Hudi) for production reliability.

## 4) Quick Anti-Patterns
- Partition by `user_id` or raw timestamp
- Thousands of tiny files per day
- Renaming/dropping columns without validating downstream dependencies
- Enabling schema merge globally for all reads without need
