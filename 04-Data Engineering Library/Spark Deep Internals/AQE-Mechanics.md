# AQE Mechanics

## Overview
Adaptive Query Execution (AQE) lets Spark revise parts of the physical execution plan at runtime after it has seen actual shuffle output statistics. Instead of committing fully to a static plan based only on compile-time estimates, Spark can react to real partition sizes and data distribution as the job runs.

High-level idea:
- Spark creates an initial physical plan
- A shuffle boundary materializes real runtime statistics
- AQE uses those statistics to re-optimize downstream plan sections
- Spark executes the updated plan instead of blindly sticking to the original choice

Important distinction:
- Catalyst optimizer improves the logical plan before execution
- AQE adapts the physical plan during execution

Interview-safe line:
- "AQE lets Spark make better runtime decisions after it sees actual shuffle sizes rather than relying only on static estimates."

## Where AQE Fits in Execution
1. Spark builds a normal physical plan.
2. Stages before a shuffle execute.
3. Shuffle outputs produce real metrics such as partition sizes.
4. AQE re-optimizes the remaining plan using those runtime statistics.
5. Spark continues with updated downstream stages.

Why shuffle boundaries matter:
- AQE needs concrete runtime information
- shuffle stages provide natural checkpoints where Spark can pause, observe, and re-plan

## What AQE Uses as Input
AQE mainly depends on runtime statistics collected from completed shuffle map stages, such as:
- actual partition sizes
- observed row counts or data volume
- distribution skew across partitions

Why this is better than static planning:
- table statistics may be missing or stale
- filters may reduce data much more than expected
- joins can become far smaller or more skewed than compile-time estimates suggested

## Core AQE Optimizations

### 1) Coalescing Post-Shuffle Partitions
If shuffle output partitions are much smaller than expected, AQE can merge adjacent reduce partitions so Spark does not launch lots of tiny tasks.

Example problem:
- static plan creates 200 shuffle partitions
- actual output is tiny
- Spark would otherwise schedule many small reduce tasks with poor efficiency

What AQE does:
- combines small post-shuffle partitions into fewer, larger tasks

Benefits:
- lower scheduler overhead
- better task sizing
- less tiny-task inefficiency

Practical takeaway:
- Coalescing is one of the most visible AQE wins on over-partitioned jobs

### 2) Join Strategy Switching
Spark may initially choose a shuffle-based join because static estimates say both sides are large. After execution of upstream stages, AQE may discover one side is actually small enough to broadcast.

Example:
- initial plan: sort merge join
- runtime result: filtered dimension table is much smaller than expected
- AQE switches to broadcast hash join

Why this helps:
- avoids large shuffle/sort cost on both sides
- reduces network traffic
- often shortens stage runtime significantly

Important nuance:
- AQE can improve a bad static decision, but only after relevant runtime stats become available
- it is not a magic substitute for generally good query design

### 3) Skew Join Optimization
If one or a few shuffle partitions are much larger than others, AQE can detect skew and split those oversized partitions into smaller units for more balanced work.

Example problem:
- one hot key sends a huge fraction of rows to one reducer
- most tasks finish quickly
- one skewed task becomes a long tail

What AQE does:
- identifies skewed partitions
- splits or reshapes their processing
- may replicate matching data on the other side when needed for the join strategy

Benefits:
- reduces straggler tasks
- improves cluster utilization
- shortens long-tail stage completion time

Practical takeaway:
- AQE often helps skew, but extremely bad key skew may still require data model or query changes

## How AQE Changes the Plan
AQE does not usually rebuild the entire query from scratch. It adapts downstream segments of the physical plan where runtime information justifies a better choice.

Typical changes include:
- fewer post-shuffle partitions
- different join operator choice
- skew-aware partition handling

Mental model:
- static plan says "based on estimates, this is probably good"
- AQE says "now that we know what actually happened, let's improve the next part"

## Common AQE Scenarios

### When AQE helps a lot
- filtered join inputs shrink dramatically at runtime
- default shuffle partition count is too high for actual data volume
- mild to moderate skew appears in wide transformations
- table statistics are missing or inaccurate

### When AQE helps less
- no meaningful shuffle boundaries exist
- data is already well-sized and well-distributed
- UDF-heavy logic or poor query shape dominates runtime
- extreme skew or bad partition keys require manual redesign

AQE improves execution choices, but it cannot fully rescue fundamentally inefficient pipelines.

## AQE vs Static Config Thinking
Before AQE, engineers often tuned jobs around fixed assumptions:
- fixed shuffle partition count
- fixed join strategy hints
- fixed expectations about data size

AQE reduces the need for some manual tuning by reacting to actual runtime behavior.

But this does not mean:
- partition count no longer matters at all
- join hints are always unnecessary
- bad data layout can be ignored

Practical rule:
- Use AQE as a smart runtime correction layer, not as a replacement for sound partitioning and query design

## What to Look for in Plans
In `explain()` output or Spark UI, AQE-related behavior often appears as:
- adaptive plans
- post-shuffle partition coalescing
- changed join operators
- skew-handling markers in join execution

What this means in practice:
- the original physical plan may differ from the final executed adaptive plan
- when debugging, inspect the executed plan rather than assuming the initial plan tells the full story

## Common Performance Wins from AQE
- fewer tiny reduce tasks after coalescing
- switching from sort merge join to broadcast hash join
- less long-tail latency from skewed partitions
- better resource utilization when runtime data differs from expectations

## Performance Cost and Production Practice

### AQE overhead
- small extra runtime overhead from collecting shuffle stats and re-optimizing downstream stages
- usually worth it for medium/large jobs with joins, shuffle, or skew
- can be less helpful for tiny or very stable jobs

### Production guidance
- keep AQE enabled by default in production
- improve code when AQE is repeatedly rescuing a bad query shape
- do not rewrite code just to mirror every adaptive plan change

### Hints or disabling AQE
Use hints or disable AQE only for narrow, measured edge cases:
- one specific query or workload
- repeated evidence that AQE makes a worse choice
- benchmarked proof that a forced strategy performs better

Practical rule:
- clean code + AQE on is usually the best production setup

## Common Misunderstandings
- "AQE fixes all skew problems"
  - It helps many skew cases, but severe skew may still need salting, repartitioning, or key redesign.

- "AQE always makes jobs faster"
  - AQE often helps, but the benefit depends on whether runtime stats reveal a meaningfully better plan.

- "If AQE is enabled, I do not need to think about shuffle partitions"
  - AQE can coalesce, but wildly bad partitioning choices can still hurt.

- "AQE is a logical optimizer"
  - It is a runtime physical-plan adaptation mechanism.

## Config Knobs to Know
Common context-dependent settings include:
- `spark.sql.adaptive.enabled`
- `spark.sql.adaptive.coalescePartitions.enabled`
- `spark.sql.adaptive.skewJoin.enabled`
- `spark.sql.adaptive.advisoryPartitionSizeInBytes`
- `spark.sql.autoBroadcastJoinThreshold`

Guideline:
- enable AQE first
- observe actual plan and task metrics
- tune only if runtime behavior suggests a specific issue

## Debugging Checklist
1. Confirm AQE is enabled for the job.
2. Compare initial and executed physical plans.
3. Check whether post-shuffle partitions were coalesced.
4. See whether a shuffle join switched to broadcast.
5. Look for skewed task durations even after AQE.
6. If performance is still poor, inspect query shape, partition keys, and data skew directly.

## Interview Angle

### Good concise answer
- "AQE allows Spark to re-optimize the physical plan at runtime using actual shuffle statistics, mainly to coalesce small partitions, switch join strategies, and mitigate skew."

### Stronger follow-up answer
- "Its biggest value is correcting bad assumptions: if a filtered dataset becomes small enough to broadcast or if shuffle partitions are much smaller or more skewed than expected, AQE can adapt instead of forcing the original static plan."

## Why It Matters
Understanding AQE helps you:
- explain why Spark sometimes executes a different plan than the one you expected
- diagnose tiny-task overhead, skewed reducers, and bad join choices
- reduce manual tuning by letting runtime statistics guide execution
- distinguish logical optimization problems from runtime physical adaptation opportunities

## Related
- [[04-Data Engineering Library/Spark Deep Internals/Catalyst-Optimizer-Rule-Catalog.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Shuffle-Fetch-Protocol.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Join-Algorithms.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Performance-Tuning-Guide.md]]
