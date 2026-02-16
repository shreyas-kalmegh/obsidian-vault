# CAP Theorem (Atomic Note)

## Core idea
In the presence of network partitions, a distributed system can choose between consistency and availability.

... (content continues as in original)

---FILE: 04-Data Engineering Library/Processing/Spark - Deep Dive - Shuffle & Memory.md
# Spark Deep Dive — Shuffle Mechanics & Memory Management

## Overview
This deep dive explains shuffle internals and memory management in Apache Spark (3.x), focusing on how data moves between tasks, when and why spills occur, and practical tuning guidance for personal projects.

## Shuffle architecture
- Map stage writes shuffle files:
  - Each map task partitions its output by reducer (shuffle partition).
  - Data is written to local disk in map output files.
- Reduce tasks fetch map outputs over the network (or from local disk for same-node tasks).
- External shuffle service can preserve shuffle data across executor restarts.

## File formats & index
- Map outputs are often written as `.map` files with an index that lists offsets per partition.
- Consolidated shuffle file formats reduce filesystem pressure (e.g., consolidated shuffle file).

## Memory regions
- Execution memory: used for shuffles, sorts, joins, aggregation buffers.
- Storage memory: cached RDDs/DataFrames and broadcast variables.
- Unified memory management (Tungsten) allows dynamic borrowing between execution and storage memory.

## When spills happen
- Sort-based shuffle spills when memory allocated for sort buffers is insufficient.
- Hash-based aggregation spills when hash table grows beyond available execution memory.
- Large number of partitions increases metadata overhead and can increase IO.

## Tuning guidelines (practical)
- Reduce shuffle size by rethinking partitioning keys.
- Increase `spark.memory.fraction` only if you have headroom and need more execution memory.
- Use `spark.sql.shuffle.partitions` tuned to data size (avoid default 200 blindly).
- Avoid too many small files — coalesce/partition wisely.

## Observability
- Use Spark UI to inspect shuffle read/write sizes, spill counts, memory usage.
- Metrics: `MemoryManager`, `ShuffleReadMetrics`, `ShuffleWriteMetrics`, `TaskMetrics`.

## Rust/Python relevance
- Arrow memory layout matters for zero-copy transfers between JVM and native code.
- Rust-based UDFs or native executors can reduce GC pressure; consider using JNI carefully.
