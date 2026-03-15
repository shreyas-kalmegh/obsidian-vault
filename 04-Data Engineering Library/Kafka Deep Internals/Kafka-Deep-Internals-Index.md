# Kafka Deep Internals Index

## How To Use This Index
Read these notes in order if you want a clean mental model from core storage internals to operational and interview-level topics. The sequence starts with how Kafka stores data, then moves into replication and control-plane behavior, and finally covers producer, consumer, and scaling concerns.

## Recommended Reading Order
### Phase 1: Storage And Data Model Foundations
1. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Log-Segment-Structure.md]]
2. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Message-Format-Internals.md]]
3. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Log-Compaction-Engine.md]]

Why first:
- These explain how Kafka physically stores records, batches, indexes, and compacted state.

### Phase 2: Replication, Durability, And Failover
4. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Replication-Internals.md]]
5. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-ISR-Management.md]]
6. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Leader-Election.md]]
7. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-KIP-500-Controller-Quorum.md]]
8. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Rack-Awareness.md]]

Why next:
- This layer explains how Kafka stays available, elects leaders, and preserves acknowledged data.

### Phase 3: Producer Path
9. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Producer-Internals.md]]
10. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Producer-Reliability.md]]
11. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Exactly-Once-Semantics.md]]

Why here:
- Once replication is clear, producer reliability settings and EOS become much easier to reason about.

### Phase 4: Consumer Path
12. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Consumer-Protocol.md]]
13. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Offset-Commit-Protocol.md]]
14. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Consumer-Rebalancing.md]]

Why here:
- These notes explain how consumers fetch, track progress, and coordinate group membership.

### Phase 5: Performance, Operations, And Capacity
15. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Network-Layer.md]]
16. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Throughput-Optimizations.md]]
17. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Throttling.md]]
18. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Scaling-Strategies.md]]
19. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Monitoring-KPIs.md]]

Why last:
- These depend on understanding the write path, read path, and replication model first.

## Fast-Track Paths
### For Data Engineering Interviews
1. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Cheatsheet.md]]
2. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Replication-Internals.md]]
3. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-ISR-Management.md]]
4. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Producer-Reliability.md]]
5. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Consumer-Protocol.md]]
6. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Exactly-Once-Semantics.md]]
7. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Interview-Questions-Data-Engineering.md]]

### For Production Debugging
1. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Monitoring-KPIs.md]]
2. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Replication-Internals.md]]
3. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-ISR-Management.md]]
4. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Consumer-Rebalancing.md]]
5. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Throughput-Optimizations.md]]
6. [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Throttling.md]]

## Companion Notes
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Cheatsheet.md]] for quick recall
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Interview-Questions-Data-Engineering.md]] for DE-focused interview preparation
