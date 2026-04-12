# Spark Structured Streaming Deep Dive

## Overview
Structured Streaming is Spark's streaming engine built on top of the same DataFrame and Spark SQL model used for batch processing. Instead of writing a completely different streaming API, you describe transformations on an unbounded table and Spark incrementally executes them as new data arrives.

High-level idea:
- input stream is treated like an ever-growing table
- query logic is expressed with DataFrame/SQL operations
- Spark runs the query incrementally in micro-batches or continuous-style execution
- checkpoints and state management let the engine recover and continue safely

Why it matters:
- it gives one programming model for batch and streaming
- production behavior depends heavily on state, watermarks, sinks, and checkpointing
- many streaming problems are not about syntax but about correctness, latency, and state growth

Interview-safe line:
- "Structured Streaming treats streaming data as an unbounded table and incrementally updates results using the same DataFrame/SQL model as batch Spark."

## Execution Model

### Unbounded table model
Spark conceptually sees the stream as a table that keeps receiving new rows.

Mental model:
- source adds new rows
- query transforms those rows
- sink receives incremental result updates

### Micro-batch by default
Most Structured Streaming jobs run in micro-batch mode.

What that means:
- Spark groups available new data into small batches
- each batch is executed as a Spark job
- latency is low, but not true record-by-record processing

### Continuous processing
Spark also has continuous-style processing support in narrower scenarios.

Practical rule:
- most real production workloads use micro-batch mode

## Core Concepts

### Source
Where streaming data comes from.

Common examples:
- Kafka
- files arriving in a directory/object store
- rate source for testing

### Sink
Where output goes.

Common examples:
- console for debugging
- memory sink for testing
- Kafka
- Delta or file sink
- custom `foreachBatch`

### Trigger
Controls when Spark processes available data.

Examples:
- process as soon as possible
- fixed interval micro-batch
- once/available-now style batch-like processing over new data

### Checkpoint
Checkpointing stores progress and state metadata so the query can recover after failure.

Practical takeaway:
- in production, checkpointing is not optional

## Output Modes

### Append
Only new final rows are written.

Best for:
- streams where old results do not need updating
- event streams without stateful rewrites of past output

### Update
Only changed rows are written.

Best for:
- aggregations where previously emitted groups can still change

### Complete
Entire result table is rewritten every trigger.

Best for:
- limited state or debugging

Practical rule:
- complete mode is often too expensive for large production stateful queries

## Stateful vs Stateless Operations

### Stateless
Each record can be processed without remembering earlier records.

Examples:
- simple filters
- projections
- parsing
- some enrichment joins with static data

### Stateful
Spark must remember prior records or aggregate state across triggers.

Examples:
- aggregations over windows
- deduplication
- stream-stream joins
- sessionization

Why this matters:
- stateful queries are where correctness and performance become much harder

## Watermarks
Watermarks tell Spark how late data is allowed to arrive for event-time-based stateful operations.

Why they matter:
- without a watermark, state can grow for a very long time
- with a watermark, Spark can eventually evict old state

Tradeoff:
- larger lateness allowance improves correctness for late events
- but keeps more state in memory and storage longer

Practical rule:
- watermark choice is a correctness and cost tradeoff, not just a config detail

## Exactly-Once vs At-Least-Once Nuance
Structured Streaming is often described as fault-tolerant and exactly-once capable, but the true guarantee depends on the sink and the end-to-end design.

Useful mental model:
- Spark can track processed offsets and recover from checkpoints
- the source/sink combination determines the practical delivery guarantee
- `foreachBatch` logic can easily break clean semantics if not written carefully

Practical takeaway:
- "exactly once" is not a magic blanket guarantee for every sink and every custom write pattern

## Common Production Patterns

### Kafka -> parse -> enrich -> aggregate -> Delta
A classic event pipeline using micro-batches, watermarks, stateful aggregation, and checkpointed output.

### File ingestion with Auto Loader / directory-based source
Useful for near-real-time ingestion of arriving files.

### `foreachBatch` for custom upsert logic
Common for writing into warehouses or serving tables.

Practical warning:
- `foreachBatch` is powerful, but idempotency becomes your responsibility

## Example

```python
from pyspark.sql import functions as F

events = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "events")
    .load()
)

parsed = (
    events
    .selectExpr("CAST(value AS STRING) AS json")
    .select(F.from_json("json", schema).alias("data"))
    .select("data.*")
    .withWatermark("event_time", "10 minutes")
)

result = (
    parsed
    .groupBy(F.window("event_time", "5 minutes"), F.col("event_type"))
    .count()
)

query = (
    result.writeStream
    .outputMode("update")
    .format("delta")
    .option("checkpointLocation", "/checkpoints/events_by_type")
    .start("/tables/events_by_type")
)
```

What this shows:
- Kafka source
- parsed event stream
- event-time watermark
- stateful windowed aggregation
- checkpointed durable sink

## Common Gotchas

### Missing or unstable checkpoint location
Without a stable checkpoint path, restart and recovery behavior breaks.

### No watermark on stateful queries
State may grow for too long, causing memory/storage pressure.

### Wrong output mode
Append/update/complete semantics can produce surprising sink behavior if chosen incorrectly.

### Non-idempotent `foreachBatch`
Retries can duplicate writes if the sink logic is not designed carefully.

### Treating streaming like batch
Some batch patterns are too expensive or semantically wrong when state is unbounded.

### Stream-stream join complexity
These joins are powerful but can become very state-heavy and sensitive to watermark design.

## Performance Optimization

### Reduce input cost early
- project only needed columns
- parse only needed fields
- filter as early as possible

### Control state growth
- use watermarks where semantically valid
- avoid unbounded stateful logic
- keep grouping keys reasonable

### Choose sink strategy carefully
- use efficient sinks
- avoid overly expensive complete-mode rewrites
- make `foreachBatch` writes idempotent and efficient

### Tune trigger and batch size
- very small triggers can increase scheduling overhead
- very large batches can increase latency and state pressure

### Watch skew and partitioning
- hot keys can create long-tail batches
- stateful aggregations and joins are sensitive to skew

Practical rule:
- in streaming, state growth is often a bigger problem than raw compute cost

## What to Watch in Production
- input rate vs processed rate
- batch duration
- state store size
- event-time watermark progress
- late data behavior
- sink write latency
- restart/recovery behavior from checkpoints

Interpretation:
- processed rate below input rate suggests backlog growth
- growing state with slow watermark progress suggests state pressure
- unstable batch duration suggests skew, sink slowdown, or resource contention

## Debugging Checklist
1. Confirm source, sink, output mode, and checkpoint location.
2. Check whether the query is stateful.
3. Verify watermark design if event time is involved.
4. Inspect batch duration, input rate, and processed rate.
5. Look for state growth, skew, or sink bottlenecks.
6. Review restart behavior and idempotency assumptions.

## Interview Angle

### Good concise answer
- "Structured Streaming uses the DataFrame/Spark SQL model for unbounded data and usually runs in micro-batches, with checkpoints and state management handling fault tolerance."

### Stronger follow-up answer
- "The hardest production parts are stateful operations, watermark design, sink semantics, and keeping processing rate ahead of input rate. Performance problems are often really state-growth or sink-efficiency problems."

## Why It Matters
Understanding Structured Streaming helps you:
- design real-time pipelines with clearer correctness guarantees
- avoid state and watermark mistakes that silently hurt production jobs
- reason about latency, throughput, and recovery more accurately
- explain streaming design choices well in interviews and system discussions

## Related
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Caching-Strategies.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Debugging-Playbook.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Memory-Pressure-Diagnostics.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Serialization-Formats.md]]
