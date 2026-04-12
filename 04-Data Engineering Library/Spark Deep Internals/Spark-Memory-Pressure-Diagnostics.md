# Spark Memory Pressure Diagnostics

## Overview
Memory pressure in Spark means tasks or executors do not have enough usable memory for their working set, causing slowdowns, spilling, garbage collection churn, or outright failures. Diagnosing it well requires separating several different symptoms that are often incorrectly lumped together as just "OOM."

High-level idea:
- some jobs fail because the JVM heap is exhausted
- some jobs survive but spill heavily and become slow
- some jobs show long GC pauses even without crashing
- some jobs are killed by the container runtime even when Spark logs look ambiguous

Why it matters:
- memory pressure is one of the most common root causes of unstable Spark jobs
- the right fix depends on the actual failure mode
- simply adding more memory often hides the symptom without fixing skew, bad partitioning, or oversized shuffles

Interview-safe line:
- "In Spark, memory pressure shows up as OOM, heavy spill, or GC churn, and the key diagnostic step is figuring out which of those is actually happening."

## The Main Memory Pressure Failure Modes

### 1) Executor OOM
The executor process runs out of available memory and crashes or becomes unstable.

Typical symptoms:
- executor lost
- task retries spike
- stage eventually fails after repeated task loss
- logs mention `OutOfMemoryError`

Common causes:
- huge shuffle partitions
- oversized join or aggregation state
- large broadcasts
- too many cached datasets
- skew causing one task to hold much more state than peers

Important nuance:
- "executor lost" is not specific enough by itself
- you need logs or container events to confirm whether the cause was really OOM

### 2) Container or Pod OOMKilled
In containerized environments, the process may be killed by the platform even if Spark heap settings look reasonable.

Typical symptoms:
- executor disappears abruptly
- platform events show `OOMKilled`
- Spark reports generic executor failure

Common causes:
- memory overhead too low
- off-heap plus on-heap memory exceeding container limits
- PySpark worker memory exceeding expectations
- native or shuffle-related memory outside pure heap assumptions

Practical takeaway:
- Spark memory config and container memory limits must be reasoned about together

### 3) Heavy Spill
The job does not crash, but operators cannot keep working state in memory and repeatedly spill to disk.

Typical symptoms:
- long-running tasks
- high disk I/O
- large spill metrics in Spark UI
- stages that finish but much more slowly than expected

Common causes:
- execution memory too small for sort/join/aggregation state
- poor partition sizing
- skew
- too much shuffle volume

Practical rule:
- spill is a survival mechanism, not evidence that the job is healthy

### 4) GC Pressure
The job spends too much time reclaiming JVM memory rather than doing useful work.

Typical symptoms:
- high GC time
- tasks appear CPU-starved
- executors stay alive but throughput is poor
- heap usage oscillates heavily

Common causes:
- object-heavy RDD or Dataset code
- UDF-heavy workloads creating many JVM objects
- large deserialized caches
- poor serializer/API choices

Practical takeaway:
- high GC does not always mean you need a bigger heap; it often means the execution path is too object-heavy

## OOM Sources to Separate Clearly

### JVM heap exhaustion
This is the classic `java.lang.OutOfMemoryError` scenario.

Usually tied to:
- object-heavy code
- large aggregation or join state
- large cached datasets

### Off-heap or native pressure
Total process memory can exceed limits even when heap looks acceptable.

Usually tied to:
- off-heap memory settings
- native libraries
- Python workers
- shuffle/network buffers

### Driver memory pressure
Not all memory failures are executor-side.

Driver-side symptoms:
- failure while planning or collecting
- broadcast creation problems
- large metadata overhead
- crashes during result collection or large action materialization

Common causes:
- `collect()` on too much data
- huge broadcast-side materialization
- very large query plans or metadata structures

## How Memory Pressure Appears in Different Operators

### Joins
Memory pressure often appears in:
- broadcast build side too large
- hash join state too large
- skewed shuffle partitions during sort merge or shuffled hash join

Warning signs:
- big spill
- one or two reducers much slower than others
- repeated executor loss during join stages

### Aggregations
Hash aggregations can grow large in memory, especially with high-cardinality keys.

Warning signs:
- spill-heavy aggregation stages
- memory-sensitive reducers
- long-tail tasks from skewed key distributions

### Sorts and wide shuffles
Sorting and shuffle merge paths create large temporary structures.

Warning signs:
- sort-heavy stages with heavy spill
- big shuffle read plus long task runtime
- disk-intensive stage behavior

### Caching
Caching competes with execution memory.

Warning signs:
- execution gets slower after caching
- more spill in join/aggregation stages
- executor memory becomes unstable after `persist()`/`cache()`

## UI Metrics to Watch

### Spill metrics
- memory spill
- disk spill

Interpretation:
- high spill indicates Spark could not keep working structures in memory

### GC time
- executor/task GC time

Interpretation:
- high GC relative to task runtime suggests heap churn or object-heavy execution

### Shuffle read/write
- remote/local shuffle read
- shuffle write size

Interpretation:
- high shuffle plus spill usually means wide transformations are stressing memory

### Task time distribution
- compare fastest and slowest tasks in a stage

Interpretation:
- large spread often indicates skew, which can create memory hotspots in a few tasks

### Executor loss patterns
- repeated failures on the same stage
- failures concentrated on specific nodes or executors

Interpretation:
- may indicate local resource exhaustion, node instability, or bad partition hotspots

## Fast Triage: What the Symptom Usually Means

### If you see `OutOfMemoryError`
- inspect whether it is driver or executor side
- check stage/operator context
- verify whether skew or giant partitions are involved

### If you see heavy spill but no crash
- investigate partition sizing
- inspect joins/aggregations/sorts
- reduce shuffle volume before only increasing memory

### If you see high GC time
- look for object-heavy code paths
- prefer DataFrame/SQL over object-heavy RDD workflows when possible
- check whether caching is consuming too much heap

### If executors disappear on Kubernetes
- inspect pod events for `OOMKilled`
- review memory overhead and total container limits
- distinguish JVM heap exhaustion from container-level kill

## Common Root Causes
- too few shuffle partitions creating oversized per-task state
- too many partitions causing excess overhead and fragmented execution
- skewed keys producing hot reducers
- broadcast side larger than expected
- stale statistics leading to poor join strategy
- caching too much deserialized data
- object-heavy UDF or Dataset paths
- wide transformations over unnecessarily large datasets

## What Usually Fixes It

### Best first fixes
- filter earlier
- prune unused columns
- reduce shuffle volume
- rebalance partition sizing
- address skew explicitly
- choose a better join strategy

These usually help more than memory increases alone.

### Then consider sizing changes
- increase executor memory if the workload is fundamentally valid but undersized
- increase memory overhead for containerized or PySpark-heavy workloads
- reduce executor cores if too many concurrent tasks raise per-executor pressure
- review cache usage and persistence level

Practical rule:
- fix data shape first, then tune memory settings

## Common Misdiagnoses
- "High GC means Spark needs more executors"
  - It may instead mean the workload is too object-heavy.

- "Spill means Spark is fine because it did not crash"
  - Spill can make jobs dramatically slower and may still indicate a poor plan.

- "OOM means the dataset is too big for Spark"
  - Often it means one partition, one join side, or one skewed key is too big for one task.

- "Executor loss on Kubernetes always means Spark instability"
  - It may simply be a container `OOMKilled` event or node resource pressure.

## Diagnostic Workflow
1. Identify whether the job is crashing, spilling, or just running slowly with GC churn.
2. Check whether the problem is driver-side or executor-side.
3. Inspect Spark UI for spill, GC, shuffle volume, and task skew.
4. Map the failing stage back to joins, aggregations, sorts, or caching.
5. Confirm whether the issue is plan shape, skew, cache pressure, or container limits.
6. Apply plan/data fixes before only raising memory knobs.

## Interview Angle

### Good concise answer
- "Spark memory pressure usually shows up as executor OOM, heavy spill, or high GC, and the fastest way to diagnose it is to separate those symptoms instead of treating them as the same problem."

### Stronger follow-up answer
- "The root cause is often not just total data size but per-task state size, skew, shuffle volume, or object-heavy execution. I check spill metrics, GC time, task skew, and whether the platform killed the container before deciding on a fix."

## Why It Matters
Understanding Spark memory pressure diagnostics helps you:
- distinguish between crash-type failures and slow-but-surviving memory issues
- avoid guessing when the real problem is skew, caching, or container limits
- choose more targeted fixes than simply adding memory
- debug Spark incidents faster in both local and platform environments

## Related
- [[04-Data Engineering Library/Spark Deep Internals/Spark-on-Kubernetes.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Serialization-Formats.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Performance-Tuning-Guide.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Tungsten-Memory-Management.md]]
