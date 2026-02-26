# PySpark DataFrame API to Spark SQL Mapping Cheatsheet

Interview goal: if you know the DataFrame operation, you can express it quickly in Spark SQL.

## 0) Setup Pattern (required for SQL)
```python
# PySpark
# df is your DataFrame
# register once, then use SQL

df.createOrReplaceTempView("events")
result = spark.sql("SELECT * FROM events LIMIT 10")
```

## 1) Select, Filter, Rename

| PySpark DataFrame API | Spark SQL |
|---|---|
| `df.select("id", "name")` | `SELECT id, name FROM events` |
| `df.selectExpr("id", "amount * 1.1 AS gross")` | `SELECT id, amount * 1.1 AS gross FROM events` |
| `df.filter("amount > 100")` / `df.where(...)` | `SELECT * FROM events WHERE amount > 100` |
| `df.withColumnRenamed("old", "new")` | `SELECT old AS new, ... FROM events` |
| `df.drop("col1")` | `SELECT <all_except_col1> FROM events` |
| `df.distinct()` | `SELECT DISTINCT * FROM events` |

## 2) Null Handling, Conditionals, Dedup

| PySpark DataFrame API | Spark SQL |
|---|---|
| `df.na.fill({"city":"NA"})` | `SELECT COALESCE(city, 'NA') AS city, ... FROM events` |
| `df.na.drop(subset=["id"])` | `SELECT * FROM events WHERE id IS NOT NULL` |
| `F.when(cond, a).otherwise(b)` | `CASE WHEN cond THEN a ELSE b END` |
| `df.dropDuplicates(["id"])` | `SELECT * FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY ts DESC) rn FROM events) t WHERE rn = 1` |

## 3) Aggregations

| PySpark DataFrame API | Spark SQL |
|---|---|
| `df.groupBy("dept").count()` | `SELECT dept, COUNT(*) AS count FROM events GROUP BY dept` |
| `df.groupBy("dept").agg(F.sum("salary"), F.avg("salary"))` | `SELECT dept, SUM(salary) AS sum_salary, AVG(salary) AS avg_salary FROM events GROUP BY dept` |
| `df.agg(F.countDistinct("user_id"))` | `SELECT COUNT(DISTINCT user_id) FROM events` |
| `df.groupBy("k").pivot("status").count()` | `SELECT * FROM events PIVOT (COUNT(*) FOR status IN ('A','B','C'))` |

## 4) Sorting, Limits, Sampling

| PySpark DataFrame API | Spark SQL |
|---|---|
| `df.orderBy(F.col("ts").desc())` | `SELECT * FROM events ORDER BY ts DESC` |
| `df.limit(10)` | `SELECT * FROM events LIMIT 10` |
| `df.sample(0.1)` | `SELECT * FROM events TABLESAMPLE (10 PERCENT)` |

## 5) Joins

| PySpark DataFrame API | Spark SQL |
|---|---|
| `a.join(b, "id", "inner")` | `SELECT * FROM a INNER JOIN b ON a.id = b.id` |
| `a.join(b, "id", "left")` | `SELECT * FROM a LEFT JOIN b ON a.id = b.id` |
| `a.join(b, "id", "left_semi")` | `SELECT a.* FROM a LEFT SEMI JOIN b ON a.id = b.id` |
| `a.join(b, "id", "left_anti")` | `SELECT a.* FROM a LEFT ANTI JOIN b ON a.id = b.id` |
| `a.join(F.broadcast(b), "id")` | `SELECT /*+ BROADCAST(b) */ * FROM a JOIN b ON a.id = b.id` |

## 6) Window Functions

| PySpark DataFrame API | Spark SQL |
|---|---|
| `F.row_number().over(Window.partitionBy("k").orderBy(F.col("ts").desc()))` | `ROW_NUMBER() OVER (PARTITION BY k ORDER BY ts DESC)` |
| `F.rank().over(...)` | `RANK() OVER (...)` |
| `F.lag("amt", 1).over(...)` | `LAG(amt, 1) OVER (...)` |
| running total with `sum().over(...)` | `SUM(amt) OVER (PARTITION BY k ORDER BY ts ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` |

## 7) String, Date, Math

| PySpark DataFrame API | Spark SQL |
|---|---|
| `F.lower("email")` | `LOWER(email)` |
| `F.trim("name")` | `TRIM(name)` |
| `F.substring("code", 1, 3)` | `SUBSTRING(code, 1, 3)` |
| `F.to_date("dt")` | `TO_DATE(dt)` |
| `F.date_add("dt", 7)` | `DATE_ADD(dt, 7)` |
| `F.datediff("end", "start")` | `DATEDIFF(end, start)` |
| `F.round("amt", 2)` | `ROUND(amt, 2)` |

## 8) Arrays, Maps, JSON

| PySpark DataFrame API | Spark SQL |
|---|---|
| `F.explode("items")` | `SELECT id, EXPLODE(items) AS item FROM events` |
| `F.size("items")` | `SIZE(items)` |
| `F.array_contains("items", "x")` | `ARRAY_CONTAINS(items, 'x')` |
| `F.get_json_object("payload", "$.user.id")` | `GET_JSON_OBJECT(payload, '$.user.id')` |
| `F.from_json("payload", schema)` | `FROM_JSON(payload, 'schemaDDL')` |
| `F.to_json(F.struct("a","b"))` | `TO_JSON(NAMED_STRUCT('a', a, 'b', b))` |

## 9) Set Operations

| PySpark DataFrame API | Spark SQL |
|---|---|
| `df1.union(df2)` | `SELECT * FROM t1 UNION ALL SELECT * FROM t2` |
| `df1.unionByName(df2)` | `SELECT colA, colB FROM t1 UNION ALL SELECT colA, colB FROM t2` |
| `df1.intersect(df2)` | `SELECT * FROM t1 INTERSECT SELECT * FROM t2` |
| `df1.exceptAll(df2)` | `SELECT * FROM t1 EXCEPT ALL SELECT * FROM t2` |

## 10) CTE Pattern (interview-friendly)
```sql
WITH filtered AS (
  SELECT user_id, event_ts, amount
  FROM events
  WHERE event_date >= DATE '2026-01-01'
),
ranked AS (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts DESC) AS rn
  FROM filtered
)
SELECT user_id, event_ts, amount
FROM ranked
WHERE rn = 1;
```

## 11) Performance Hints You Can Use in SQL
- Broadcast small table: `/*+ BROADCAST(dim) */`
- Control join strategy: `/*+ MERGE(a, b) */`, `/*+ SHUFFLE_HASH(a) */`
- Partition hints: `/*+ REPARTITION(200, key) */`, `/*+ COALESCE(50) */`

## 12) Multi-Step Query Example (Repartition + Coalesce + Write)
```sql
-- Step 1: build an intermediate dataset and increase parallelism before heavy aggregation
WITH base AS (
  SELECT
    user_id,
    DATE(event_ts) AS event_date,
    amount
  FROM raw_events
  WHERE event_ts >= TIMESTAMP '2026-01-01 00:00:00'
),
daily AS (
  SELECT /*+ REPARTITION(240, event_date) */
    event_date,
    user_id,
    SUM(amount) AS daily_amount
  FROM base
  GROUP BY event_date, user_id
),
final_out AS (
  SELECT /*+ COALESCE(48) */
    event_date,
    user_id,
    daily_amount
  FROM daily
)
INSERT INTO analytics.user_daily_amount
SELECT event_date, user_id, daily_amount
FROM final_out;
```

## 13) Fast Interview Answers
- Existence check: use `LEFT SEMI JOIN`.
- Not matched rows: use `LEFT ANTI JOIN`.
- Latest record per key: `ROW_NUMBER() ... WHERE rn = 1`.
- Running totals and top-N per group: window functions.
- Replace PySpark chains with CTE blocks for readability.
