# Spark Shuffle — Practical Examples

## Local experiment with shuffle behavior
- Run small Spark jobs locally with different `spark.sql.shuffle.partitions` settings.
- Notice spill counts via Spark UI and task metrics.

## Example
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("shuffle-test").getOrCreate()
df = spark.range(0, 10_000_000)
df2 = df.repartition(200, "id")
res = df2.groupBy((df2.id % 100).alias("bucket")).count()
res.collect()
```
- Vary `repartition` and `spark.sql.shuffle.partitions` to see performance changes.
