# Spark Join Algorithms

## Overview
Spark can execute the same logical join using different physical algorithms depending on data size, join keys, sort requirements, available statistics, and runtime adaptation. The chosen join algorithm often has a larger impact on performance than the SQL syntax itself.

High-level idea:
- Logical plan says which datasets to join and on what condition
- Physical planner chooses how to perform that join
- Different algorithms trade off shuffle cost, memory usage, sort cost, and resilience to skew

Why it matters:
- joins are often the most expensive operators in Spark workloads
- a good join choice can remove large shuffles or long sort phases
- a bad join choice can create memory pressure, skewed reducers, and long-running stages

Interview-safe line:
- "Spark's main join algorithms differ in how much data they shuffle, whether they need sorting, and whether one side can fit in memory for local probing."

## The Main Join Algorithms

### 1) Broadcast Hash Join
Spark broadcasts the smaller side of the join to every executor, builds an in-memory hash table from it, and probes that hash table while scanning partitions of the larger side.

Best for:
- fact-to-dimension joins
- one side small enough to broadcast
- highly selective filters that shrink one side significantly

How it works:
1. Small side is collected/materialized for broadcast.
2. Spark distributes it to executors.
3. Each executor builds a local hash structure.
4. The large side is scanned partition by partition and probed locally.

Strengths:
- avoids shuffling the large side
- avoids global sort cost
- usually fastest when one side is truly small

Weaknesses:
- requires executor memory for the broadcast side
- risky if the "small" side is larger than expected
- may be missed if table statistics are stale

What to look for in plans:
- `BroadcastHashJoin`
- `BroadcastExchange`

## 2) Sort Merge Join
Spark repartitions both sides by join key, sorts each partition, and then merges matching key ranges.

Best for:
- large joins where neither side is small enough to broadcast
- equi-joins on sizable datasets
- cases where Spark needs a robust default for large distributed joins

How it works:
1. Both sides shuffle by join key.
2. Each shuffled partition is sorted.
3. Matching partitions are merged to produce joined rows.

Strengths:
- scales well for large datasets
- works reliably when both sides are large
- common default for big equi-joins

Weaknesses:
- expensive due to shuffle and sort on both sides
- sensitive to skew
- can produce long shuffle read and spill-heavy stages

What to look for in plans:
- `SortMergeJoin`
- `Exchange`
- `Sort`

Practical rule:
- Sort merge join is often the safe fallback, but it is rarely the cheapest option if broadcast is viable

## 3) Shuffle Hash Join
Spark shuffles both sides by join key, but instead of sorting both sides, it builds a hash table on one side within each partition and probes it with the other side.

Best for:
- cases where partition-local hash build is feasible
- some moderately sized joins where sorting cost can be avoided

How it works:
1. Both sides repartition by join key.
2. For each partition pair, Spark builds a hash table on one side.
3. The other side probes that local hash structure.

Strengths:
- can be cheaper than sort merge if partition-local hash tables fit well
- avoids full sort cost

Weaknesses:
- more memory-sensitive than sort merge join
- less favorable if partition sizes are large or skewed
- often not chosen when Spark believes sort merge is safer

What to look for in plans:
- `ShuffledHashJoin`

Mental model:
- It still pays shuffle cost, but tries to save sort cost by using partition-local hashing.

## 4) Broadcast Nested Loop Join
Spark broadcasts one side and performs nested-loop style comparison against the other side.

Best for:
- non-equi joins
- some range or complex join predicates where hash or merge strategies do not apply cleanly

Strengths:
- supports join conditions that equi-join algorithms cannot handle directly
- can still be acceptable if one side is very small

Weaknesses:
- much more expensive than broadcast hash join for large search spaces
- easy to misuse if the broadcasted side is not truly tiny

What to look for in plans:
- `BroadcastNestedLoopJoin`

Practical warning:
- If you see this unexpectedly on large data, investigate immediately

## 5) Cartesian / Cross Join Behavior
If Spark performs a true cross join, every row on one side may be paired with every row on the other side.

Why this is dangerous:
- explosive row growth
- severe CPU and memory cost
- usually indicates missing join conditions or intentionally broad analytic logic

Use with care:
- cross joins can be valid, but they should never be accidental

## How Spark Chooses a Join Algorithm
Spark considers several factors:
- join type and join condition
- size of each side
- availability and quality of statistics
- whether join keys support equi-join algorithms
- configuration thresholds
- AQE runtime adaptations

Common selection logic:
- if one side is small enough, prefer broadcast hash join
- if both sides are large for an equi-join, sort merge join is often favored
- if partition-local hashing looks feasible, shuffled hash join may be used
- if predicate type is complex or non-equi, nested loop strategies may appear

Important nuance:
- the initial plan may change under AQE after real shuffle statistics arrive

## Equi-Join vs Non-Equi Join

### Equi-join
Examples:
- `a.id = b.id`
- `orders.customer_id = customers.customer_id`

These are ideal for:
- broadcast hash join
- sort merge join
- shuffled hash join

### Non-equi join
Examples:
- `a.ts BETWEEN b.start_ts AND b.end_ts`
- `a.value > b.threshold`

These often push Spark toward:
- broadcast nested loop join
- other more expensive strategies

Practical takeaway:
- Equi-joins are much more optimization-friendly in Spark

## Join Algorithm Tradeoffs at a Glance

### Broadcast hash join
- least shuffle when one side is small
- memory cost replicated across executors
- best for classic dimension joins

### Sort merge join
- scalable for large-large joins
- heavy shuffle and sort cost
- often chosen as the robust default

### Shuffled hash join
- shuffle required, but sort may be avoided
- sensitive to partition-local memory limits
- can be good in the right size regime

### Broadcast nested loop join
- useful for some non-equi cases
- dangerous on anything but very small broadcast side

## Skew and Join Behavior
Skew affects all distributed joins, but especially shuffle-based ones.

Common pattern:
- one join key value appears far more often than others
- one or a few reducers receive much more data
- tasks become stragglers and spill heavily

Effects by join type:
- broadcast hash join: can still suffer if the large-side partitions are skewed
- sort merge join: often strongly affected by skew during shuffle and merge
- shuffled hash join: can hit both skew and memory pressure within hot partitions

What helps:
- AQE skew join handling
- salting or repartitioning strategies
- better join keys or upstream aggregation

## Statistics and AQE
Spark's join selection quality depends heavily on relation size estimates.

If statistics are good:
- Spark is more likely to pick the right broadcast opportunities
- bad shuffle-heavy plans are less likely

If statistics are bad:
- Spark may miss broadcast joins
- Spark may choose a strategy that spills or sorts unnecessarily

AQE helps by:
- switching to broadcast after runtime shrinkage
- coalescing post-shuffle partitions
- mitigating skew in some join scenarios

## What to Look for in `explain()`

### Healthy signs
- small dimension side becomes `BroadcastHashJoin`
- fewer exchanges than expected
- adaptive plan improves an initial join choice

### Warning signs
- `BroadcastNestedLoopJoin` on large relations
- repeated `Exchange` and `Sort` around big joins
- huge shuffle read and spill metrics
- one or two reducers taking far longer than peers

## Common Tuning Levers
- reduce data before the join with filters and projections
- maintain useful table statistics
- let AQE adapt runtime join choices
- use broadcast hints carefully when Spark misses an obvious small side
- avoid unnecessary repartitioning before joins
- inspect skew before only changing config values

Relevant configs often include:
- `spark.sql.autoBroadcastJoinThreshold`
- `spark.sql.adaptive.enabled`
- `spark.sql.shuffle.partitions`

Config changes help most after you understand the actual physical join behavior.

## Debugging Checklist
1. Run `explain("formatted")` and identify the actual physical join operator.
2. Check whether one side should have been broadcast but was not.
3. Look for large shuffle reads, sort time, and spill in Spark UI.
4. Compare task durations for skew symptoms.
5. Verify table statistics and filtered relation sizes.
6. Let AQE run, then inspect the executed plan rather than only the initial plan.

## Interview Angle

### Good concise answer
- "Spark mainly uses broadcast hash join, sort merge join, and shuffled hash join for equi-joins, choosing among them based on side sizes, memory feasibility, and shuffle/sort tradeoffs."

### Stronger follow-up answer
- "If one side is small, broadcast hash join is usually best because it avoids shuffling the large side. If both sides are large, sort merge join is the common scalable fallback, while shuffled hash join can help when partition-local hashing is feasible."

## Why It Matters
Understanding Spark join algorithms helps you:
- predict why a query became shuffle-heavy or memory-heavy
- choose better join shapes for fact-dimension and large-large workloads
- diagnose skew, spill, and bad broadcast decisions
- explain query plans clearly in interviews and real production debugging

## Related
- [[04-Data Engineering Library/Spark Deep Internals/AQE-Mechanics.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Shuffle-Fetch-Protocol.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Broadcast-Mechanics.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Performance-Tuning-Guide.md]]
