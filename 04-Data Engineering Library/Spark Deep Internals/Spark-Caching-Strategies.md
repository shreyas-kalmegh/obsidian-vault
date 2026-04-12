# Spark Caching Strategies

## Overview
Caching in Spark means keeping a computed dataset available for reuse so Spark does not have to recompute it from lineage every time it is referenced. Done well, caching can remove repeated scans, joins, or expensive transformations. Done badly, it can waste memory, increase GC pressure, and slow the whole application down.

High-level idea:
- Spark computes a DataFrame/RDD once
- the result is persisted in memory, disk, or both
- later actions can reuse that stored result
- Spark trades storage cost for lower recomputation cost

Why it matters:
- iterative workloads and reused intermediate datasets can become much faster with caching
- caching competes with execution memory needed for joins, sorts, and shuffle
- many Spark jobs are slower because they cache the wrong thing, or cache too much

Interview-safe line:
- "Caching helps when the same expensive intermediate result is reused multiple times, but it hurts when the cached data displaces execution memory or is never reused enough to pay for itself."

## When Caching Helps

### Reused intermediate datasets
If the same filtered or transformed dataset is used by multiple downstream actions or branches, caching can avoid repeating the same upstream work.

Examples:
- one cleaned DataFrame feeding multiple aggregations
- one expensive feature-preparation step reused in several model stages
- one dimension-like lookup dataset reused repeatedly in a notebook workflow

### Iterative or exploratory workflows
Caching is often useful in:
- interactive analysis
- notebook sessions
- repeated debugging queries
- machine learning style iterative pipelines

### Expensive lineage
If recomputing a dataset means re-reading large source data, repeating complex joins, or rerunning costly UDF logic, caching can pay off quickly.

Practical takeaway:
- cache the result of expensive reused work, not just any dataset that exists in the middle of the pipeline

## When Caching Hurts

### One-time-use datasets
If a dataset is only used once after it is computed, caching usually adds overhead without benefit.

Costs include:
- time to materialize the cache
- memory consumed by stored blocks
- possible eviction of more useful cached data

### Large datasets with low reuse
Caching a huge DataFrame that is referenced only a small number of times can be worse than recomputing it, especially if it pushes execution into spill or GC pressure.

### Execution-memory starvation
Caching competes with joins, sorts, and aggregations for memory.

Symptoms:
- more spill after caching
- slower joins after `cache()`
- executor instability or GC churn

Practical rule:
- cache is not a free speed boost; it is a memory tradeoff

## What `cache()` Really Does
Calling `cache()` or `persist()` marks a dataset for persistence, but Spark does not populate the cache immediately. The data is usually cached only when an action actually materializes it.

Typical flow:
1. You call `cache()`.
2. Spark keeps the logical intent to persist the dataset.
3. The next action computes the dataset.
4. Computed partitions are stored according to the chosen storage level.
5. Future actions may reuse those stored partitions.

Important nuance:
- `cache()` is lazy, like many Spark transformations
- if you want to intentionally materialize the cache, trigger an action such as `count()`

## Storage Levels
Spark supports several persistence strategies, each trading memory footprint, recomputation cost, and CPU overhead differently.

## 1) Memory-only
Store partitions in memory only.

Strengths:
- fastest reuse if the cached data fits
- avoids disk reads on reuse

Weaknesses:
- if partitions do not fit, some may be evicted or recomputed
- can create strong GC pressure if data is deserialized and object-heavy

Best for:
- moderately sized, frequently reused datasets
- workloads where fast repeated access matters more than memory efficiency

## 2) Memory and disk
Store as much as possible in memory and spill the rest to disk.

Strengths:
- more resilient than pure memory-only caching
- avoids full recomputation when memory is insufficient

Weaknesses:
- disk-backed reuse is slower than memory-backed reuse
- still consumes storage resources and may increase I/O

Best for:
- reused datasets that do not fit fully in memory
- practical workloads where recomputation is expensive

## 3) Disk-only
Persist only to disk.

Strengths:
- avoids recomputing expensive lineage
- reduces memory pressure relative to in-memory storage

Weaknesses:
- much slower to reuse than memory-backed persistence
- useful less often for pure performance acceleration

Best for:
- very expensive lineage when memory is limited
- cases where fault tolerance/reuse matters more than raw speed

## 4) Serialized vs deserialized storage
Spark can persist data in a more compact serialized form or in a deserialized/object form depending on the API path and storage level.

Serialized storage:
- lower memory footprint
- more CPU needed to decode on reuse
- often better when memory is the bottleneck

Deserialized storage:
- faster direct access in some cases
- higher memory use
- can increase GC pressure

Practical takeaway:
- serialized storage saves memory; deserialized storage may save CPU

## Memory vs Disk Tradeoffs

### Memory-heavy caching
Pros:
- fastest repeated access
- good for iterative computation

Cons:
- competes with execution memory
- can trigger GC pressure
- may cause eviction if the working set is too large

### Disk-backed caching
Pros:
- cheaper in memory terms
- avoids full recomputation

Cons:
- slower reuse
- can increase local disk I/O
- less helpful if the downstream workflow is latency-sensitive

Practical rule:
- if recomputation is cheap, do not overvalue persistence
- if recomputation is expensive, disk-backed persistence can still be worth it

## Cache Eviction
Cached data is not guaranteed to stay in memory forever. Spark may evict cached blocks when memory is needed elsewhere.

Why eviction happens:
- execution memory pressure grows
- too many datasets are cached
- cached data simply does not fit

What eviction means in practice:
- some partitions may be dropped from memory
- future actions may need disk reads or recomputation
- cache hit behavior can become inconsistent across stages

Practical takeaway:
- caching is not the same as pinning data permanently in memory

## Unified Memory Interaction
Caching lives inside Spark's broader unified memory model, where storage memory and execution memory interact.

Why this matters:
- aggressive caching can reduce space available for joins, aggregations, and sorts
- execution-heavy stages may evict cached blocks
- apparent caching benefits may disappear under heavy shuffle workloads

Practical rule:
- if a job is shuffle-heavy, be careful about large caches competing with execution state

## Best Candidates for Caching
- reused intermediate DataFrames with expensive lineage
- filtered datasets reused in multiple branches
- notebook exploration datasets repeatedly queried
- iterative feature engineering or ML preparation results

## Poor Candidates for Caching
- one-shot outputs used once
- datasets larger than memory with little reuse
- raw source tables that are cheap to rescan from efficient columnar storage
- highly volatile intermediate data that changes every step

## Caching vs Checkpointing
Caching and checkpointing are related but solve different problems.

Caching:
- primarily improves reuse performance
- preserves lineage
- may be evicted

Checkpointing:
- truncates lineage
- helps with fault recovery or very long lineage graphs
- usually involves more durable storage semantics

Practical takeaway:
- cache for speed
- checkpoint for lineage management and resilience

## Common Failure Patterns

### Cache created but never reused
Symptoms:
- memory consumed
- no meaningful speedup

Cause:
- dataset cached too early or without enough downstream reuse

### Cache causes more spill
Symptoms:
- joins/aggregations become slower after caching
- spill metrics increase

Cause:
- cached data reduced execution memory too much

### Cache causes high GC
Symptoms:
- executors stay busy but throughput drops
- GC time rises sharply

Cause:
- deserialized/object-heavy cached data occupying too much heap

### Cache unexpectedly recomputes
Symptoms:
- repeated work despite `cache()`
- inconsistent speedups

Cause:
- eviction, lineage recomputation, or cache never fully materialized

## Practical Best Practices
- cache only after you know the dataset will be reused
- cache after expensive filtering or joins, not blindly at the source
- materialize the cache intentionally if reuse timing matters
- unpersist datasets that are no longer useful
- choose serialized storage when memory pressure matters more than decode CPU
- validate whether caching improved end-to-end runtime instead of assuming it did

## A Simple Decision Framework

### Ask these questions
1. Will this dataset be reused multiple times?
2. Is recomputing it actually expensive?
3. Will caching it starve execution memory?
4. Does it fit reasonably in the chosen storage level?
5. Would checkpointing be more appropriate than caching?

If the answer to reuse or recomputation cost is weak, caching is probably not worth it.

## What to Watch in Spark UI
- storage tab: cached RDD/DataFrame footprint and partition status
- stage spill metrics after caching
- executor memory pressure and GC
- whether downstream stages get faster after the cache is materialized

Interpretation:
- if storage usage rises but stage runtime does not improve, the cache may not be paying for itself
- if spill or GC worsens after caching, the cache may be hurting the workload

## Debugging Checklist
1. Confirm the cached dataset is actually reused.
2. Check whether the cache was materialized by an action.
3. Inspect storage footprint and whether partitions are being evicted.
4. Compare runtime before and after caching.
5. Look for spill or GC regressions caused by reduced execution memory.
6. Unpersist caches that are no longer needed.

## Interview Angle

### Good concise answer
- "In Spark, caching is useful when the same expensive intermediate result is reused multiple times, but it can backfire if it consumes memory needed for joins, sorts, and shuffle."

### Stronger follow-up answer
- "I choose storage levels based on whether memory or recomputation is the bigger cost. Memory-only is fastest if it fits, memory-and-disk is a practical fallback, and I always verify that the cache materially reduces total runtime instead of assuming it helps."

## Why It Matters
Understanding Spark caching strategies helps you:
- decide when persistence will genuinely improve performance
- avoid slowing jobs by caching the wrong datasets
- balance storage memory against execution memory needs
- explain cache-related regressions, eviction, and recomputation clearly

## Related
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Checkpointing.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Memory-Pressure-Diagnostics.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Performance-Tuning-Guide.md]]
