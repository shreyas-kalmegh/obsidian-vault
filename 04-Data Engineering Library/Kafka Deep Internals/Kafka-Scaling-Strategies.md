# Kafka Scaling Strategies

## Overview
Scaling Kafka is about balancing partition count, broker capacity, consumer parallelism, replication overhead, and operational complexity. More partitions help parallelism, but they also increase metadata and coordination cost.

## Common Scaling Levers
- Add partitions to increase parallelism.
- Add brokers to spread storage and leadership.
- Separate hot topics from cold ones.
- Use compression and batching to reduce network and disk pressure.

## Partition Scaling
- More partitions increase producer and consumer concurrency.
- Too many partitions increase open files, metadata size, and rebalance cost.
- Partition count should reflect expected throughput and consumer parallelism, not just an arbitrary round number.

## Broker Scaling
- Adding brokers helps only if partitions and leadership are redistributed.
- New brokers with little traffic are a common anti-pattern after rushed scaling.

## Hot Partition Mitigation
- Use better partition keys.
- Add key salting where ordering requirements allow.
- Split very hot entities into separate topics if needed.

## Example
A topic has 8 partitions and one partition handles 40% of traffic due to customer ID skew.

Possible fixes:
- redesign partition key
- add a derived sharding suffix
- isolate that workload into a dedicated topic

Simply adding brokers will not fix a single hot partition if the key distribution stays skewed.

## Interview Angle
- Kafka scale limits are often partition-design limits before broker CPU limits.
- Adding brokers without rebalancing data or leadership changes little.
- Partition count is a long-term design decision because increasing it can affect ordering and downstream behavior.

## Related
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Throughput-Optimizations.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Consumer-Rebalancing.md]]
