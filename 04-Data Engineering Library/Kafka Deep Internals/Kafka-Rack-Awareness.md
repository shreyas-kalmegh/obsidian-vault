# Kafka Rack Awareness

## Overview
Rack awareness spreads replicas across failure domains such as racks, availability zones, or data centers. The goal is to reduce the chance that one infrastructure failure removes all replicas of a partition.

## How It Works
- Brokers are tagged with a rack or zone identifier.
- Kafka attempts to place partition replicas across different racks.
- This improves resilience against localized infrastructure failures.

## Example
Three brokers:
- `B1` in `zone-a`
- `B2` in `zone-b`
- `B3` in `zone-c`

For replication factor 3, Kafka can place one replica in each zone.  
If `zone-b` fails, the partition can still survive with replicas in `zone-a` and `zone-c`.

## Tradeoffs
- Better fault tolerance across zones
- Higher inter-zone network cost
- Possible increase in replication latency if zones are far apart

## Operational Notes
- Rack awareness is most useful when rack labels reflect real failure boundaries.
- Bad metadata, such as identical rack labels everywhere, defeats the point.
- Leader placement still matters for client latency even if replica placement is safe.

## Interview Angle
- Rack awareness is about resilience and placement, not about consumer partition assignment.
- It complements replication factor; it does not replace it.
- Cross-zone design always trades durability against latency and cost.

## Related
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-ISR-Management.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Scaling-Strategies.md]]
