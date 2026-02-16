# Asynchronous Checkpoints

## Overview
This document provides a medium-depth explanation of *Asynchronous Checkpoints*, covering how Flink implements this mechanism and why it matters for real-time, stateful stream processing.

## Key Sections
- **Async Snapshot Threads**: Medium-depth description covering core mechanics.
- **State Copying**: Medium-depth description covering core mechanics.
- **Write Amplification**: Medium-depth description covering core mechanics.
- **Restore Behavior**: Medium-depth description covering core mechanics.

## Why It Matters
Understanding **Asynchronous Checkpoints** is essential when building reliable, high-throughput streaming pipelines, diagnosing performance issues, and tuning state-heavy workloads.

## Related
- [[04-Data Engineering Library/Flink Deep Internals/Checkpoint-Alignment.md]]
