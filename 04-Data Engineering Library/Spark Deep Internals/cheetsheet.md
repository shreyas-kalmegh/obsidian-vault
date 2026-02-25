# Spark Coding Interview Cheatsheet (High ROI)

## Quick Decision Table

| Interview Situation | First Choice | Why |
|---|---|---|
| ETL with joins + aggregates | DataFrame API / Spark SQL | Catalyst + Tungsten optimize it |
| Need row-level custom logic | Built-in functions first, UDF last | UDFs block optimizations |
| Small dim + large fact join | Broadcast join | Avoid expensive shuffle |
| Slow join on skewed key | Salting / AQE skew join / pre-agg | Prevent straggler tasks |
| OOM during shuffle | Repartition, reduce wide ops, tune memory/partitions | Less spill + better parallelism |

---

## 1) Spark Mental Model (What to Say in Interview)

- Driver builds a logical plan.
- Catalyst optimizer rewrites query plan.
- Physical plan executes as stages with tasks.
- Wide transformations (joins/groupBy/orderBy) create shuffle boundaries.

High ROI statement:
- "I’ll minimize shuffles, use built-in expressions, and verify plan via `explain` before tuning config knobs."

---

## 2) Transformations vs Actions

Transformations are lazy (`select`, `filter`, `join`, `groupBy`).
Actions trigger execution (`count`, `collect`, `show`, `write`).

```python
df2 = df.filter("status = 'ok'").select("id", "ts")  # lazy
n = df2.count()  # action -> job runs
```

Gotcha:
- Multiple actions on same expensive lineage recompute unless cached.

---

## 3) High-ROI DataFrame Patterns

### Filter early, project narrow
```python
result = (
    df.filter("event_date >= '2026-01-01'")
      .select("user_id", "event_date", "amount")
)
```

### Prefer built-ins over Python UDF
```python
from pyspark.sql import functions as F

df = df.withColumn("norm_email", F.lower(F.trim("email")))
```

Why:
- Built-ins are optimized and JVM-native.
- Python UDF causes serialization overhead and limited optimization.

---

## 4) Joins: Pattern and Performance

### Broadcast join (small dimension)
```python
from pyspark.sql import functions as F

joined = fact.join(F.broadcast(dim), "key", "left")
```

### Join types to know
- `inner`, `left`, `right`, `full`, `left_semi`, `left_anti`

Interview tip:
- Use `left_semi` / `left_anti` for existence checks (fewer columns + often cheaper).

Gotchas:
- Joining on differently typed keys causes implicit cast + poor performance.
- Duplicate column names after join can silently cause confusion.

---

## 5) Window Functions (Frequent Interview Topic)

```python
from pyspark.sql import Window, functions as F

w = Window.partitionBy("user_id").orderBy(F.col("event_time").desc())
latest = (
    df.withColumn("rn", F.row_number().over(w))
      .filter("rn = 1")
      .drop("rn")
)
```

Use for:
- latest-per-entity
- top-N per group
- running sums and lag/lead

Gotcha:
- Window + huge partitions can be expensive; repartition by key first when appropriate.

---

## 6) Aggregations and Distinct

```python
agg = (
    df.groupBy("country")
      .agg(
          F.count("*").alias("rows"),
          F.countDistinct("user_id").alias("users"),
          F.sum("amount").alias("revenue"),
      )
)
```

Gotchas:
- `countDistinct` is expensive at scale.
- Consider `approx_count_distinct` if approximation is acceptable.

---

## 7) Partitioning, Repartition, Coalesce

- `repartition(n)` -> full shuffle, increases/decreases partitions.
- `coalesce(n)` -> reduce partitions with less shuffle (good for final writes).

```python
df = df.repartition(400, "user_id")
out = df.coalesce(50)
```

Gotcha:
- Too many tiny partitions -> scheduler overhead.
- Too few huge partitions -> skew/OOM/slow tasks.

---

## 8) Data Skew Handling

Symptoms:
- A few tasks run much longer.
- One reducer has huge input.

Fixes:
1. Enable AQE skew handling.
2. Pre-aggregate before join.
3. Salt hot keys.
4. Broadcast small side where possible.

Salting sketch:
```python
from pyspark.sql import functions as F

left_salted = left.withColumn("salt", (F.rand() * 16).cast("int"))
right_expanded = right.crossJoin(spark.range(16).toDF("salt"))
joined = left_salted.join(right_expanded, ["key", "salt"])
```

---

## 9) Caching and Persistence

```python
hot = expensive_df.persist()  # MEMORY_AND_DISK default in many APIs
hot.count()  # materialize cache
```

Use cache when:
- Same DataFrame reused across multiple actions/stages.

Do not cache when:
- Data used once.
- Data too large to fit and causes heavy eviction.

Always unpersist when done.

---

## 10) File Formats and I/O

Preferred:
- Parquet/ORC for analytical workloads.

```python
(df.write
   .mode("overwrite")
   .partitionBy("event_date")
   .parquet("s3://bucket/path"))
```

High ROI practices:
- Partition by low/moderate cardinality columns used in filters.
- Avoid too many small files.
- Use predicate pushdown and column pruning.

Gotchas:
- Over-partitioning write path creates metadata and small-file explosion.

---

## 11) Adaptive Query Execution (AQE)

AQE can improve:
- join strategy selection at runtime
- skew partition handling
- post-shuffle partition coalescing

Common configs to know:
- `spark.sql.adaptive.enabled=true`
- `spark.sql.adaptive.skewJoin.enabled=true`

Interview note:
- Still design good queries; AQE is not a substitute for poor modeling.

---

## 12) Debugging and Plan Inspection

```python
df.explain("formatted")
```

Look for:
- number of exchanges (`Exchange` = shuffle)
- join type (`BroadcastHashJoin`, `SortMergeJoin`)
- scan pruning (only required columns)

Operational checks:
- Spark UI: stage DAG, skewed tasks, spill metrics, shuffle read/write.

---

## 13) Common Interview Gotchas

- Using `collect()` on large data -> driver OOM.
- Python UDF where SQL function exists.
- Joining before filtering/projection.
- Repartitioning repeatedly without reason.
- Ignoring data skew.
- Writing many tiny files.
- Not handling null-safe join conditions when needed.
- Assuming `orderBy` without partitioning is cheap (global sort is expensive).

---

## 14) Performance Tuning Checklist (Practical)

1. Confirm correctness first with small sample.
2. Check physical plan (`explain`).
3. Reduce shuffle count (push filters, pre-agg, proper join choice).
4. Choose join strategy (broadcast vs sort-merge).
5. Fix skew (AQE, salting, pre-aggregation).
6. Tune partition count (`spark.sql.shuffle.partitions`, repartition by key).
7. Cache only reused expensive intermediates.
8. Optimize write path (file count, partition columns, format).
9. Validate via Spark UI (task skew, spill, shuffle size).

---

## 15) 60-Second Interview Answer Template

- "I’ll start with DataFrame/Spark SQL using built-in functions."
- "I’ll filter and project early to reduce data volume before joins."
- "For joins, I’ll broadcast small dimensions and watch for skew on large keys."
- "I’ll inspect `explain`/Spark UI and optimize shuffles and partitioning."
- "If reused, I’ll cache selectively; then optimize write layout to avoid small files."
