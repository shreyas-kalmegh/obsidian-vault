# Kafka Monitoring KPIs

## Overview
Kafka monitoring should cover throughput, latency, durability, consumer progress, and cluster balance. Looking at only one metric, such as CPU or lag, usually hides the real bottleneck.

## Broker Health KPIs
- `UnderReplicatedPartitions`: non-zero deserves attention.
- `OfflinePartitionsCount`: critical, indicates unavailable partitions.
- Request handler idle percent: low values suggest saturation.
- Network processor idle percent: low values suggest socket or network pressure.
- Disk usage and log flush latency: reveal storage bottlenecks.

## Producer-Side KPIs
- Produce request latency
- Record send rate
- Record retry rate
- Error rate
- Batch size and compression ratio

## Consumer-Side KPIs
- Consumer lag by group and partition
- Rebalance rate
- Poll loop latency
- Commit latency and commit failure rate

## Replication KPIs
- ISR shrink and expand rate
- Follower fetch lag
- Leader election rate
- Unclean leader election count

## Example Debug Pattern
Symptoms:
- consumer lag rising
- broker CPU moderate
- request latency stable
- ISR healthy

Likely causes:
- slow consumer processing
- not enough consumers
- max poll or fetch sizing issues

If instead lag rises with ISR shrink and produce latency spikes, look first at broker IO or network issues.

## Practical Dashboard Rules
- Always pair lag with throughput.
- Separate transient spikes from sustained degradation.
- Track per-topic and per-partition outliers, not just cluster averages.

## Interview Angle
- `UnderReplicatedPartitions` is usually a better durability early warning than raw CPU.
- Consumer lag is not always a broker problem.
- Election count, ISR churn, and request latency together tell a better story than any single metric.

## Related
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-ISR-Management.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Throughput-Optimizations.md]]
