# Kafka Throughput Optimizations

## Overview
Kafka throughput comes from batching, sequential IO, compression, partition parallelism, and efficient network usage. Most throughput wins come from shaping traffic into larger, steadier batches.

## Main Optimization Areas
- Producer batching
- Compression choice
- Sufficient partitions for parallelism
- Network and IO thread sizing
- Fast disks and healthy page cache behavior

## Producer-Side Levers
- Increase `batch.size` where payload size supports it.
- Use small positive `linger.ms` to form larger batches.
- Enable compression, often `lz4` or `zstd` depending on workload.
- Avoid overly chatty per-record flush patterns.

## Broker-Side Levers
- Ensure adequate `num.network.threads` and `num.io.threads`.
- Use storage with strong sequential write performance.
- Keep replication healthy so leaders are not blocked by lagging followers.

## Consumer-Side Levers
- Increase fetch sizes for large sequential reads.
- Use enough consumers and partitions to match required read parallelism.
- Avoid expensive per-message downstream processing in the critical path.

## Example
A producer sending 1 KB messages one by one:
- no compression
- `linger.ms=0`
- small batches

After tuning:
- `linger.ms=10`
- larger `batch.size`
- `lz4` compression

Result:
- fewer requests
- better compression ratio
- lower network cost
- usually higher broker throughput

## Interview Angle
- Kafka throughput is usually a batching problem before it is a CPU problem.
- Compression often increases throughput because it reduces bytes on the wire and disk.
- More partitions help only when producers and consumers can actually use the extra parallelism.

## Related
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Producer-Internals.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Network-Layer.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Monitoring-KPIs.md]]
