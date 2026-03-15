# Kafka Interview Questions For Data Engineering

## How To Use This Note
- Aim for concise, systems-oriented answers.
- Tie Kafka internals to data engineering tradeoffs: reliability, latency, replay, and scaling.
- In interviews, prefer concrete examples over textbook definitions.

## Core Questions
### 1. Why does Kafka scale well for event streaming workloads?
Because it uses partitioned append-only logs, sequential disk IO, batching, compression, and pull-based consumers. Throughput comes from partition parallelism and large efficient batches rather than per-message coordination.

### 2. What is ISR and why is it important?
ISR is the set of replicas that are sufficiently caught up with the leader. It determines safe acknowledgements, high watermark advancement, and clean leader election behavior.

### 3. Explain `acks=0`, `acks=1`, and `acks=all`.
- `acks=0`: producer does not wait for broker acknowledgement.
- `acks=1`: leader acknowledges after local write.
- `acks=all`: leader waits for required in-sync replicas.

For production pipelines carrying important data, `acks=all` with appropriate `min.insync.replicas` is usually the durability baseline.

### 4. Why can duplicates still happen in Kafka pipelines?
Retries, consumer replays after crash, and external sink writes can all create duplicates. Idempotent producers solve retry duplicates inside Kafka, but end-to-end exactly-once requires careful sink design or transactions.

### 5. What is the difference between at-least-once and exactly-once?
- At-least-once allows replay and therefore possible duplicates.
- Exactly-once in Kafka means duplicate-free committed output for supported transactional workflows, mainly consume-process-produce pipelines inside Kafka.

### 6. What happens during a consumer rebalance?
The group coordinator redistributes partitions when members join, leave, time out, or when subscriptions change. Work may pause or partially pause, and uncommitted progress handling becomes important.

### 7. Why is consumer lag not enough by itself to diagnose a problem?
Lag is an outcome metric. The root cause may be slow consumers, poor partitioning, broker IO problems, ISR shrink, long processing stages, or downstream sink slowness.

### 8. How does Kafka ensure ordering?
Kafka guarantees ordering only within a partition. If ordering across entities matters, the partition key must route related records to the same partition.

### 9. When would you use log compaction?
For latest-state topics such as user profiles, dimension tables, CDC upserts, and stream processing changelogs where rebuilding current state matters more than preserving every historical version.

### 10. What changes with KIP-500 / KRaft?
Kafka removes ZooKeeper and stores metadata in a Raft-based controller quorum. That simplifies operations and makes metadata management Kafka-native.

## Scenario Questions
### 11. Producer latency rose sharply after enabling TLS. What would you check?
- CPU overhead on brokers and clients
- network thread saturation
- request latency distribution
- cipher and handshake overhead
- whether batch sizes became too small relative to per-request cost

### 12. Consumer lag is growing, but broker CPU is low. What does that suggest?
Likely consumer-side or downstream bottlenecks: slow processing, too few consumers, poll interval issues, sink latency, or bad fetch sizing.

### 13. A topic has replication factor 3, but one broker failure still caused write failures. Why?
Replication factor alone is not enough. ISR may have already shrunk, and `min.insync.replicas` plus `acks=all` may no longer be satisfiable after the failure.

### 14. You added brokers but throughput barely improved. Why?
Possible reasons:
- partitions were not redistributed
- hot partitions remained hot
- consumer parallelism did not increase
- bottleneck is downstream system rather than Kafka

### 15. When is unclean leader election acceptable?
Only when availability matters more than the risk of losing acknowledged messages. For most critical data engineering pipelines, it is avoided.

## Strong Follow-Up Points
- Mention high watermark when discussing safe reads after failover.
- Mention `__consumer_offsets` when discussing progress tracking.
- Mention idempotence vs transactions separately.
- Mention partition-key design when discussing scale or ordering.

## Related
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Cheatsheet.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Exactly-Once-Semantics.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Replication-Internals.md]]
