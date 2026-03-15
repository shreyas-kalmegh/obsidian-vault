# Kafka, Flink, Pinot: High-Value Interview Questions

## Kafka
- Explain Kafka delivery semantics: at-most-once, at-least-once, and exactly-once. What configuration and tradeoffs are required for each?
- How do idempotent producers and transactional producers work internally, and when is each necessary?
- What happens during a consumer group rebalance? Compare eager vs cooperative rebalancing and their impact on latency.
- How do you choose partition count for a topic, and what are the implications for throughput, ordering, and future scaling?
- What is ISR, leader election, and `min.insync.replicas`? How do these settings affect durability and availability?
- Describe how Kafka handles backpressure when consumer lag grows. What are concrete remediation steps?
- How do compaction and retention interact? When would you use compacted topics vs delete retention topics?
- How do you design keys and partition strategy to avoid hot partitions while preserving required ordering?
- What are common causes of duplicate processing in Kafka pipelines, and how do you mitigate them end to end?
- How do schema evolution and compatibility work with Avro/Protobuf + Schema Registry in multi-team environments?
- What metrics and alerts are most important for Kafka brokers and consumers in production?
- Describe how MirrorMaker 2 or Cluster Linking helps in DR/multi-region, and what consistency limits remain.
1. At-most-once commits before processing; at-least-once commits after processing; exactly-once uses idempotent producer + transactions, with higher latency/complexity.
2. Idempotence deduplicates producer retries per partition; transactions atomically write to topics and commit consumer offsets together.
3. Rebalance reassigns partitions; eager pauses all consumers, cooperative reassigns incrementally and reduces disruption.
4. Partitions set parallelism ceiling; more partitions improve throughput but increase overhead and make key-level ordering only partition-local.
5. ISR are in-sync replicas; `min.insync.replicas` with `acks=all` improves durability but can reduce availability during broker loss.
6. Consumer lag grows under slow processing; scale consumers, tune batch/poll settings, increase partitions, and optimize downstream sinks.
7. Compaction keeps latest record per key; delete retention keeps all data for time/size window; choose by replay/audit vs latest-state use case.
8. Use stable high-cardinality keys and maybe salting/sharding for hot keys, while preserving required ordering within logical key scope.
9. Duplicates come from retries, rebalance replays, and sink failures; mitigate with idempotent writes, transactions, dedupe keys, and idempotent sinks.
10. Schema Registry enforces compatibility rules (backward/forward/full); add optional fields and avoid breaking type changes.
11. Monitor broker disk/network/under-replicated partitions/request latency and consumer lag/rebalance rate/commit latency.
12. MM2/Cluster Linking replicate topics for DR, but failover is typically eventually consistent with possible lag and offset translation concerns.

## Flink
- Explain Flink checkpointing vs savepoints. When would you use each, and what operational risks exist?
- How does Flink achieve exactly-once state consistency with checkpoint barriers, and where can this guarantee break?
- Describe event time vs processing time vs ingestion time. Why does event time matter for correctness?
- How do watermarks work, and how do you choose watermark strategy for out-of-order events?
- Compare tumbling, sliding, and session windows. What correctness/performance tradeoffs do they introduce?
- How do allowed lateness and side outputs for late data work, and how do they affect downstream aggregates?
- Explain keyed state, operator state, and RocksDB state backend choices. When is each appropriate?
- What is state TTL and how do you prevent unbounded state growth in long-running jobs?
- How does Flink handle backpressure, and which metrics show where the bottleneck is?
- What happens during rescaling a Flink job with large state? How does state redistribution work?
- Explain two-phase commit sinks and exactly-once sinks (for example Kafka, Iceberg, JDBC) with failure scenarios.
- In Flink SQL/Table API, what are common pitfalls around changelog semantics (append/upsert/retract streams)?
1. Checkpoints are periodic fault-tolerance snapshots; savepoints are operator-controlled snapshots for upgrades/migrations.
2. Barrier alignment snapshots consistent state plus source offsets; guarantees can break with non-transactional sinks or side effects.
3. Event time reflects when event occurred and is needed for correct windows under delays; processing time is arrival-time dependent.
4. Watermarks signal event-time progress; pick strategy based on observed delay distribution and acceptable lateness.
5. Tumbling gives fixed non-overlapping windows, sliding overlaps for smoother trends, session is gap-based for bursty behavior.
6. Allowed lateness updates closed windows within tolerance; side outputs capture too-late events for separate correction pipelines.
7. Keyed state is per key, operator state is per task; RocksDB fits large state and heap backend fits smaller low-latency state.
8. State TTL expires inactive keys, plus compaction/timers and key design prevent unbounded state growth.
9. Backpressure propagates upstream when an operator is slow; use busy time, backpressured time, and checkpoint duration metrics.
10. Rescaling redistributes keyed state by key-group mapping; large state increases restore time and network shuffle cost.
11. Two-phase commit writes pending data and commits on successful checkpoint, preventing duplicates on failures.
12. SQL pitfalls include misreading retract/upsert streams as append-only and incorrect primary key/change-log assumptions.


## Pinot
- Explain Pinot architecture: controller, broker, server, minion, and segment store. What does each component do?
- What is the difference between real-time and offline tables in Pinot, and when do you use hybrid tables?
- How does Pinot consume from Kafka in real-time ingestion, and what offset/consumption guarantees apply?
- What is a segment in Pinot, and how do segment size and flush thresholds impact query latency and ingestion cost?
- Compare star-tree index, inverted index, range index, bloom filter, and text index. When should each be used?
- How do you design schema and table config to support high-cardinality dimensions and low-latency aggregations?
- What is upsert in Pinot, and how do primary key + comparison columns affect correctness?
- How do partial upserts work, and what are common mistakes when modeling mutable events?
- Explain time boundary in hybrid tables and how Pinot routes queries across real-time/offline segments.
- How do replica groups and partitioning improve query isolation and scalability?
- Which Pinot metrics would you monitor for query SLA, ingestion health, and segment movement issues?
- Describe common causes of query slowness in Pinot and a systematic tuning approach.
1. Controller manages metadata, broker routes queries, server stores/serves segments, minion runs background tasks, deep store holds segment files.
2. Real-time ingests streaming data, offline serves batch segments, hybrid combines both for freshness plus historical completeness.
3. Pinot low-level/high-level consumers read Kafka partitions and track offsets; guarantee is usually at-least-once ingestion.
4. Segment is Pinot’s storage/query unit; too small increases overhead, too large hurts pruning/latency and recovery flexibility.
5. Star-tree accelerates grouped aggregations, inverted helps equality filters, range for range filters, bloom for existence pruning, text for search.
6. Model dimensions/measures carefully, precompute derived fields, and configure indexes on frequent filters/group-bys.
7. Upsert keeps latest row by primary key using comparison column ordering; wrong comparison logic causes stale results.
8. Partial upsert updates only selected columns; mistakes include missing default/null handling and unordered updates.
9. Time boundary splits query range between offline and real-time segments to avoid overlap gaps/duplicates.
10. Replica groups isolate query load and partitioning limits scanned data, improving parallelism and tail latency.
11. Track P95/P99 query latency, segment load failures, consuming lag, LLC commit lag, and server CPU/memory.
12. Slowness usually comes from bad indexes, high-cardinality scans, skew, or segment bloat; tune with query profiling and index redesign.

## Cross-System Design Questions (Kafka + Flink + Pinot)
- Design a near-real-time analytics pipeline from Kafka to Flink to Pinot with exactly-once or effectively-once guarantees.
- How do you handle late, duplicate, and out-of-order events so Pinot dashboards remain accurate?
- Where would you enforce deduplication: Kafka producer, Flink job, Pinot upsert, or multiple layers?
- How do you plan backfills/reprocessing without breaking Pinot serving freshness?
- What is your strategy for schema evolution across Kafka topics, Flink transformations, and Pinot tables?
- How do you design for multi-region failover while keeping recovery time low and data loss bounded?

## Short Answers

### Kafka (in same order as questions)


### Flink (in same order as questions)

### Pinot (in same order as questions)


### Cross-System (in same order as questions)
1. Use Kafka idempotent/transactional producers, Flink event-time processing + checkpointing, and Pinot upsert/hybrid tables for low-latency serving.
2. Use watermarks + allowed lateness in Flink, dedupe keys/stateful operators, and Pinot upsert on primary key with proper comparison column.
3. Best practice is layered: producer idempotence, Flink dedupe for stream correctness, and Pinot upsert as serving-side safety net.
4. Run backfill into separate topics/tables, validate, then cut over or merge to avoid impacting fresh real-time segments.
5. Govern schemas centrally (Schema Registry + versioning), enforce compatibility checks, and roll out producer/consumer/table changes in sequence.
6. Use region-local Kafka/Flink/Pinot with async replication, define RPO/RTO targets, and automate failover with controlled offset recovery.
