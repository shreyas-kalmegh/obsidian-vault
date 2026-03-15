# Kafka Throttling

## Overview
Kafka throttling controls how fast clients or replication flows can consume broker resources. It protects cluster stability during overload, replica movement, or noisy-neighbor scenarios.

## Main Throttle Types
- Client quotas for producers or consumers
- Replication throttles during partition reassignment
- Controller or admin-operation rate limits in some environments

## Why Throttling Exists
- Prevent a single tenant from saturating broker network or IO
- Keep replication catch-up from starving client traffic
- Smooth large reassignments and migrations

## Example
During partition reassignment:
- leader sends large replica data to new broker
- without throttle, client request latency may spike
- with replication throttle, migration takes longer but cluster remains usable

## Operational Notes
- Too little throttling risks cluster instability.
- Too much throttling can create long recovery windows.
- Quotas should match business priority and workload class, not just technical identity.

## Interview Angle
- Throttling is a fairness and stability mechanism, not only a performance penalty.
- Reassignment throttle is often a deliberate tradeoff: slower maintenance for safer production traffic.
- Good Kafka operations distinguish between client-path traffic and internal replication traffic.

## Related
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Network-Layer.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Scaling-Strategies.md]]
