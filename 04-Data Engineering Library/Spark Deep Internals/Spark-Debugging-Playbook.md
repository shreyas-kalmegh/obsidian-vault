# Spark Debugging Playbook

## Overview
Spark debugging gets easier when you stop treating every incident as a brand-new mystery and instead follow a repeatable triage flow. Most Spark problems reduce to a small set of root-cause families:
- too much data movement
- bad join or partitioning choices
- skew
- memory pressure
- platform/runtime failures
- plain correctness bugs in logic or schema handling

High-level idea:
- first identify whether the job is slow, failing, or returning wrong results
- then isolate the failing or slow stage
- inspect the physical plan and Spark UI metrics for that stage
- only after that move into logs, platform events, and config tuning

Why it matters:
- many teams waste time tuning configs before understanding the actual bottleneck
- Spark exposes enough signals to narrow most problems quickly if you read them in the right order
- a structured debugging workflow is much faster than reading logs at random

Interview-safe line:
- "My Spark debugging approach is: identify the symptom, isolate the stage, inspect the physical plan and Spark UI, then map the metrics back to a small set of likely causes like shuffle, skew, memory, or bad join strategy."

## Step 1: Classify the Problem
Before touching configs, decide which of these you are dealing with:

### Slow but succeeds
Typical meanings:
- heavy shuffle
- skew
- spill
- poor join choice
- too many tiny tasks

### Fails intermittently
Typical meanings:
- executor loss
- network/shuffle fetch instability
- container/node instability
- memory pressure near the edge

### Fails consistently at the same stage
Typical meanings:
- deterministic bad plan
- bad join or aggregation state size
- schema/data issue
- repeated skew hotspot

### Produces wrong results
Typical meanings:
- logic bug
- join condition issue
- null handling problem
- schema evolution or parsing issue

Practical rule:
- do not mix correctness debugging with performance debugging until you know which one you are solving

## Step 2: Find the Bad Stage
Most Spark incidents are stage-specific.

Questions to answer:
- which stage is slowest or failing?
- is the problem tied to shuffle read, shuffle write, join, sort, aggregation, or cache usage?
- are all tasks slow, or only a few?

Why this matters:
- "the job is slow" is too broad
- you usually need the one problematic stage and its operator shape

What to inspect first:
- stage duration
- task duration spread
- shuffle read/write size
- spill metrics
- executor failures for that stage

## Step 3: Read the Physical Plan
Use `explain()` or the executed plan to answer:
- what join algorithm is Spark using?
- where are the exchanges and sorts?
- are filters and projections pushed early enough?
- is AQE changing the plan at runtime?

Common things to look for:
- `BroadcastHashJoin` vs `SortMergeJoin`
- repeated `Exchange`
- `BroadcastNestedLoopJoin`
- big aggregation or sort operators
- adaptive plan changes

Practical takeaway:
- many Spark bugs become obvious once you look at the physical plan instead of only the SQL text

## Diagnosing Slowness

### Symptom: whole stage is slow
Likely causes:
- large shuffle volume
- poor partition count
- expensive sort/aggregation
- reading too much data

Fast checks:
- stage shuffle read/write
- scan size
- whether filters and column pruning happened
- task counts and average task runtime

### Symptom: one or a few tasks are much slower
Likely causes:
- skew
- oversized partition
- hot key in join or aggregation
- executor/node-local issue

Fast checks:
- task duration spread
- per-task input sizes
- skewed keys or partition imbalance
- whether slow tasks concentrate on one executor

### Symptom: many tiny tasks with scheduler overhead
Likely causes:
- too many shuffle partitions
- tiny input files
- over-partitioned downstream stages

Fast checks:
- number of tasks vs actual data volume
- average task runtime
- file count and partition count

## Shuffle Failures
Shuffle failures are among the most common Spark failure families.

Typical symptoms:
- `FetchFailedException`
- stage retries
- executor lost during shuffle-heavy stage
- reducers waiting a long time or repeatedly failing

Likely causes:
- executor that produced shuffle data died
- local disk or shuffle files disappeared
- network timeout or instability
- skewed reducer causing extreme pressure
- shuffle partitions too large

Fast debugging sequence:
1. Identify whether failure happens during shuffle read or write.
2. Check whether executors disappeared before fetch failures began.
3. Look for disk pressure, local storage issues, or `OOMKilled` events.
4. Inspect skew and reducer size distribution.
5. Reduce shuffle volume or rebalance partitions before only increasing retry settings.

Practical rule:
- retry-related configs can improve resilience, but they do not fix unhealthy shuffle design

## Skew Debugging
Skew means a small number of partitions or keys hold a disproportionate amount of data or work.

Typical symptoms:
- one or a few tasks run far longer than others
- stage is "almost done" but waits on stragglers
- spill or OOM occurs only in a few tasks
- joins or aggregations behave unpredictably on large data

Where skew shows up most:
- joins
- groupBy / aggregations
- repartitioning by uneven keys

Fast checks:
- compare longest and shortest task times
- compare shuffle read size per task
- inspect key distribution if available
- see whether AQE skew handling changed the plan

Common fixes:
- salting hot keys
- changing partition key strategy
- pre-aggregating before the heavy join
- letting AQE skew optimization help
- broadcasting a small side when appropriate

## Memory and Spill Debugging

### Symptom: executor OOM or container kill
Likely causes:
- too-large per-task state
- big broadcast side
- skew
- insufficient memory overhead in containers

### Symptom: heavy spill, but no crash
Likely causes:
- sort/join/aggregation state larger than execution memory
- poor partition sizing
- wide shuffle-heavy stage

### Symptom: high GC
Likely causes:
- object-heavy RDD or Dataset path
- UDF-heavy logic
- large deserialized caches

Fast checks:
- spill metrics
- GC time
- stage operator type
- executor loss pattern
- whether problem is cluster-specific or reproducible locally

Practical rule:
- distinguish memory crash, spill slowdown, and GC churn before choosing a fix

## Reading Spark Logs
Logs are useful, but only after you know what stage or symptom you are investigating.

What logs help with:
- exact exception type
- stack trace location
- repeated executor failure patterns
- schema parsing and serialization problems
- driver-side planning or action failures

What logs usually do not tell you by themselves:
- whether the root cause was skew
- whether a join strategy was bad
- whether partition sizing caused the issue

Practical takeaway:
- use logs to confirm the failure mechanism, not as your only debugging tool

## Reading Platform Signals
In Kubernetes, YARN, or managed cloud environments, some failures are not visible clearly in Spark logs alone.

Examples:
- pod `OOMKilled`
- node disk pressure
- pending executors
- image/dependency failures
- network policy or DNS issues

Why this matters:
- Spark may report generic executor loss even when the platform knows the exact reason

## Wrong Results Debugging
Not every Spark incident is about performance.

Common correctness issues:
- duplicate rows after incorrect join keys
- lost rows from join type mistakes
- null handling mistakes
- schema mismatch or silent type coercion
- timestamp/timezone parsing issues

Fast checks:
- validate row counts at each major step
- inspect join conditions carefully
- sample problematic records
- compare schema before and after transformations
- reduce to a tiny reproducible local dataset

Practical rule:
- if the answer is wrong, optimize later

## A Useful Symptom-to-Cause Map

### Slow stage + huge shuffle read
- likely wide transformation or bad join shape

### Slow stage + one long tail task
- likely skew or oversized partition

### Slow stage + high spill
- likely execution memory pressure

### High GC + modest shuffle
- likely object-heavy code path or cache pressure

### Repeated executor loss + platform events
- likely container/node/runtime issue

### `BroadcastNestedLoopJoin` unexpectedly
- likely non-equi join or planner fallback that needs attention

## A Practical Debugging Workflow
1. Identify whether the issue is slowness, failure, or wrong output.
2. Find the exact stage and operators involved.
3. Inspect Spark UI for shuffle, spill, skew, and task distribution.
4. Read the physical/executed plan.
5. Check logs for exact exception or failure confirmation.
6. If on a platform, inspect pod/container/node events too.
7. Apply plan/data fixes before config-only fixes.
8. Re-test on a representative workload, not just a tiny happy-path sample.

## Common Debugging Mistakes
- tuning configs before reading the plan
- blaming Spark when the issue is platform scheduling or storage
- assuming more memory solves skew
- trusting local mode timings as production evidence
- ignoring row-count validation when results are wrong
- changing multiple variables at once and losing signal

## Interview Angle

### Good concise answer
- "I debug Spark by first classifying the issue as slowness, failure, or wrong output, then isolating the specific stage, checking the physical plan and Spark UI metrics, and finally confirming the exact failure mode from logs and platform events."

### Stronger follow-up answer
- "Most issues collapse into a few buckets: shuffle-heavy plans, skew, memory pressure, bad join choice, or platform instability. The fastest path is to find the bad stage, inspect task distribution and spill/shuffle metrics, and then fix plan shape before tuning knobs."

## Why It Matters
Understanding a Spark debugging playbook helps you:
- move from vague symptoms to specific root causes faster
- avoid wasting time on random config changes
- debug both Spark-engine and platform/runtime problems more systematically
- build a repeatable incident response habit for data pipelines

## Related
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Memory-Pressure-Diagnostics.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-UI-Metrics-Explained.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Shuffle-Fetch-Protocol.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Performance-Tuning-Guide.md]]
