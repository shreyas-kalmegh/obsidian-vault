# Tungsten Memory Management

## Overview
Project Tungsten is Spark's low-level execution and memory optimization effort focused on reducing JVM object overhead, improving CPU efficiency, and managing data in compact binary formats. Its memory-management ideas are a major reason Spark SQL and DataFrame execution are far more efficient than older object-heavy execution paths.

High-level idea:
- JVM objects are expensive in memory and garbage collection cost
- Tungsten prefers compact binary representations and explicit memory management
- Spark stores and processes internal data in layouts that are cheaper to scan, copy, and aggregate
- when memory pressure rises, Spark spills managed data structures to disk instead of failing immediately

Why it matters:
- memory pressure is one of the most common causes of slow or unstable Spark jobs
- Tungsten explains why modern Spark uses `UnsafeRow`, off-heap options, and spill-heavy execution structures
- understanding this layer helps explain GC issues, spill behavior, and why built-in SQL paths outperform object-heavy code

Interview-safe line:
- "Tungsten reduces Spark's dependence on expensive JVM objects by using compact binary data formats and more explicit memory management."

## What Tungsten Optimizes
Tungsten is not one single feature. It is a set of execution ideas centered on:
- compact binary row storage
- reduced object allocation
- explicit memory pages and bookkeeping
- CPU-friendly execution paths
- controlled spilling under memory pressure

Useful mental model:
- old style: many Java objects, pointer chasing, high GC overhead
- Tungsten style: binary memory blocks, fewer objects, tighter loops, better cache behavior

## Binary Row Format
One of Tungsten's most important building blocks is the use of compact internal binary row representations such as `UnsafeRow`.

Why binary rows help:
- fields can be read by offset rather than by chasing object references
- null tracking is compact
- fixed-width values are efficient to access
- serialization/deserialization overhead is reduced inside Spark's engine

Benefits:
- less JVM heap overhead
- lower GC pressure
- faster scans, joins, and aggregations

Practical takeaway:
- Spark is fastest when it can stay in its internal binary formats rather than bouncing through rich JVM objects

## Off-Heap Buffers
Tungsten can use off-heap memory for some execution structures, meaning memory is allocated outside the normal JVM heap.

Why off-heap can help:
- reduces garbage collector pressure
- avoids creating large numbers of JVM-managed objects
- gives Spark more direct control over memory layout and lifetime

Tradeoff:
- win: less GC overhead and more predictable memory use for some workloads
- cost: memory becomes less visible to normal JVM heap monitoring and must be managed carefully

Important nuance:
- off-heap is an optimization tool, not a free memory expansion trick
- if total memory demand is too high, off-heap will not save a fundamentally oversized workload

## Page Allocation Model
Spark often manages Tungsten memory in pages or blocks rather than allocating many tiny objects individually.

Conceptually:
1. Spark requests a memory page from its execution-memory manager.
2. Operators store rows, hash maps, sort buffers, or aggregation state inside that page.
3. When full, Spark may request more pages or spill existing data structures.

Why page allocation helps:
- fewer small allocations
- less allocator overhead
- easier bookkeeping for managed execution structures

Mental model:
- instead of millions of scattered JVM objects, think of larger managed memory arenas holding compact binary data

## Execution Memory vs Storage Memory
Spark's unified memory model is closely related to Tungsten-style execution.

Two important buckets:
- execution memory: used for joins, sorts, aggregations, shuffles
- storage memory: used for cached/persisted data

Why this matters:
- execution-heavy jobs compete with cached data for memory
- under pressure, Spark may evict cached blocks or spill execution structures
- memory issues are often caused by the interaction between these two uses, not just one operator in isolation

Practical takeaway:
- a heavily cached cluster can still have poor join/sort performance if execution memory becomes constrained

## Operators That Rely on Tungsten Memory Heavily
Tungsten-backed memory structures are especially important in:
- hash aggregation
- sort-based operations
- shuffle read/write buffers
- broadcast hash join build side
- shuffled hash join structures

These operators often keep internal state in managed binary memory until they must spill.

## Spill Behavior
When Spark cannot keep a working data structure in memory, it spills part of that state to disk.

Common spill scenarios:
- sort buffers exceed available execution memory
- aggregation hash maps grow too large
- shuffle-related structures need more memory than available

Why spilling exists:
- it allows jobs to continue under memory pressure
- it is much better than failing immediately

But spilling is still expensive:
- disk I/O increases
- merge work increases
- CPU overhead can rise
- task runtime often becomes much longer

Practical rule:
- spilling is a safety valve, not a sign of an efficient plan

## What Happens During Spill
At a high level:
1. Operator fills in-memory buffers or hash structures.
2. Memory manager cannot satisfy more requests cheaply.
3. Spark spills part of the structure to disk.
4. Processing continues with refreshed memory.
5. Later Spark merges or rereads spilled segments as needed.

Examples:
- sort spills create sorted runs that must later be merged
- aggregation spills may require multi-phase merge/combine behavior

## Why GC Improves with Tungsten
Traditional object-heavy processing creates many short-lived objects and pointers, which increases GC work.

Tungsten reduces this by:
- storing more data in binary pages
- reusing internal buffers
- avoiding per-row object materialization where possible

Result:
- less heap churn
- fewer GC pauses
- better CPU time spent on actual computation

Important nuance:
- GC issues do not disappear completely
- user code, UDFs, dataset encoders, and object-heavy transformations can still reintroduce GC pressure

## Tungsten and Whole-Stage Codegen
Tungsten and whole-stage codegen work together closely.

Useful split:
- Tungsten: efficient binary memory layout and managed memory behavior
- whole-stage codegen: efficient generated row-processing code

Together they help Spark:
- process `UnsafeRow` data efficiently
- minimize object creation
- keep execution in a CPU- and memory-efficient path

## Common Failure and Slowdown Patterns

### Heavy spill
Symptoms:
- long task runtimes
- large spill metrics in Spark UI
- high disk I/O during joins or aggregations

Likely causes:
- undersized execution memory
- skewed partitions
- too-large hash/sort state
- poor partition sizing

### Executor OOM
Symptoms:
- executor lost
- container killed
- repeated task retries and failures

Likely causes:
- data structures too large for available memory
- broadcast side larger than expected
- skew causing hot partitions
- off-heap plus on-heap combined memory exceeding container limits

### High GC despite Tungsten
Symptoms:
- long GC pauses
- low CPU efficiency
- memory churn

Likely causes:
- UDF-heavy object creation
- Dataset/object APIs instead of staying on optimized SQL paths
- cached object-heavy structures

## What to Look for in Spark UI
- spill metrics for tasks and stages
- executor memory instability
- skewed task runtimes
- large shuffle read/write combined with spill
- high GC time relative to task execution

Interpretation:
- high spill with long tasks usually means execution memory pressure
- high GC with modest spill often points to object-heavy code paths
- one or two very slow tasks suggest skew more than generic low memory

## Tuning Levers

### First fix plan shape and data movement
- reduce shuffled data volume
- prune columns
- filter early
- broadcast when appropriate
- address skew

This usually matters more than low-level memory tuning.

### Then review memory behavior
- right-size executor memory
- consider off-heap settings only when you understand the workload
- avoid over-caching large datasets that compete with execution memory
- watch partition sizing so per-task state is reasonable

Common context-dependent settings include:
- `spark.memory.fraction`
- `spark.memory.storageFraction`
- `spark.memory.offHeap.enabled`
- `spark.memory.offHeap.size`

Guideline:
- do not tune memory knobs in isolation from plan shape, partitioning, and skew

## Common Misunderstandings
- "Off-heap means Spark won't OOM"
  - It can still OOM at the process or container level if total memory demand is too high.

- "Spill is normal so it is fine"
  - Some spill is survivable, but heavy spill is usually a performance problem.

- "Tungsten fixes all memory issues automatically"
  - It improves the engine, but bad partitioning, skew, and oversized broadcasts still hurt badly.

- "GC problems mean Spark is not using Tungsten"
  - Tungsten reduces GC pressure, but user code can still create many JVM objects.

## Debugging Checklist
1. Check whether the stage is spill-heavy, shuffle-heavy, or GC-heavy.
2. Inspect the physical plan for joins, sorts, and aggregations driving large state.
3. Look for skewed partitions before only increasing memory.
4. Verify whether broadcasts or caches are consuming too much memory.
5. Distinguish JVM heap pressure from total process/container memory pressure.
6. Optimize query shape before leaning on memory configs alone.

## Interview Angle

### Good concise answer
- "Tungsten improves Spark performance by storing internal data in compact binary formats and managing memory more explicitly, which reduces object overhead and GC cost."

### Stronger follow-up answer
- "Its biggest practical impact is on joins, sorts, and aggregations: Spark keeps working state in compact memory pages, spills when needed, and pairs this with code generation so execution is faster and less object-heavy."

## Why It Matters
Understanding Tungsten memory management helps you:
- explain why Spark SQL is faster than object-heavy execution paths
- diagnose spill, GC pressure, and executor OOM issues more accurately
- connect binary row formats, off-heap memory, and execution-state management
- tune Spark with a better mental model of what the engine is doing internally

## Related
- [[04-Data Engineering Library/Spark Deep Internals/Columnar-Execution-Engine.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Performance-Tuning-Guide.md]]
- [[04-Data Engineering Library/Spark Deep Internals/WholeStageCodegen-Internals.md]]
