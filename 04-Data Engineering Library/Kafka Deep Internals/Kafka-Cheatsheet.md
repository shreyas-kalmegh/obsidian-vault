# Kafka Deep Internals Cheatsheet

## Core Mental Model
- Producer writes to partition leader.
- Followers pull from leader.
- ISR defines which replicas are caught up enough for safe acknowledgements and elections.
- Consumers pull data and manage progress through committed offsets.

## Durability Quick Lookup
| Goal | Key Settings / Concepts | Notes |
| --- | --- | --- |
| Low latency, weak durability | `acks=0` or `acks=1` | Fast, but leader failure can lose data |
| Stronger write durability | `acks=all`, `min.insync.replicas>=2` | Requires healthy ISR |
| Retry without duplicates | `enable.idempotence=true` | Per-partition retry dedupe |
| Consume-process-produce EOS | transactions + `read_committed` | Strongest inside Kafka pipelines |

## Replication Quick Lookup
| Term | Meaning |
| --- | --- |
| Leader | Handles client reads and writes |
| Follower | Pulls data from leader |
| ISR | Replicas considered sufficiently caught up |
| High Watermark | Safely replicated offset boundary |
| Leader Epoch | Leadership generation for divergence recovery |

## Consumer Quick Lookup
| Topic | Key Point |
| --- | --- |
| Fetch | Pull-based, consumer controls pace |
| Commit | Stored in `__consumer_offsets` |
| Auto Commit | Easy but easy to misuse |
| Rebalance | Partition redistribution on membership changes |
| Cooperative Rebalance | Less disruptive than eager rebalance |

## Storage Quick Lookup
| File | Purpose |
| --- | --- |
| `.log` | Record batches |
| `.index` | Sparse offset lookup |
| `.timeindex` | Timestamp lookup |
| `.txnindex` | Transaction metadata assistance |

## Compaction Vs Retention
| Mechanism | Keeps |
| --- | --- |
| Time / size retention | Data within age or size window |
| Log compaction | Latest value per key plus tombstone window |

## Common Failure Interpretation
| Symptom | Likely Area |
| --- | --- |
| Rising lag, healthy brokers | Slow consumers or low consumer parallelism |
| ISR shrink | Broker disk/network/GC issues |
| High retry rate | Producer path instability or broker overload |
| Frequent rebalances | Heartbeat, poll, or membership instability |
| Slow reassignment | Replication throughput or throttle limits |

## Interview One-Liners
- Kafka durability is controlled by ISR health, acknowledgements, and `min.insync.replicas`, not replication factor alone.
- Consumers are pull-based because backpressure belongs at the consumer.
- High watermark prevents exposing unreplicated records after failover.
- Idempotence is not the same as exactly-once semantics.

## Related
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Replication-Internals.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Producer-Reliability.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Consumer-Protocol.md]]
