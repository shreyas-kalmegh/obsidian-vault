# Flink Deep Dive — Checkpointing, State Backends, and Exactly-Once Semantics

## Overview
Flink provides strong semantics for stateful stream processing. This deep dive covers checkpointing, state backends (RocksDB vs memory), and how exactly-once processing works.

## Checkpointing basics
- Coordinator (JobManager) triggers checkpoints periodically.
- Each operator snapshots its state and writes to a durable storage (e.g., S3).
- Barrier alignment ensures consistent snapshot across distributed operators.
- Asynchronous snapshots: state is copied without pausing the operator (fast).

## State backends
- MemoryStateBackend: keeps state in memory; checkpoints to local fs (small state only).
- FsStateBackend: stores state in TaskManager memory, checkpoints to file system.
- RocksDBStateBackend: stores state in RocksDB (local), snapshots are incremental to durable storage — preferred for large states.

## Exactly-once guarantees
- With checkpointing + two-phase commit sinks (or transactional sinks), Flink can provide end-to-end exactly-once semantics.
- Checkpoint barriers ensure a consistent cut; sinks must be idempotent or support transactions.

## Watermarks & event time
- Watermarks tell operators the progress of event time.
- Late data handling strategies: allowed lateness, side outputs for late records.

## Tuning tips
- Use incremental checkpoints with RocksDB to reduce snapshot size.
- Tune checkpoint interval and timeout: aggressive intervals increase overhead; long intervals risk recovery time.
- Monitor checkpoint alignment durations and checkpoint sizes.

## Integration with Kafka
- Flink’s Kafka source can use offsets committed as part of checkpoint; this enables exactly-once consumption with proper sink handling.
