# Kafka ISR Management

## Overview
ISR stands for in-sync replicas. It is the set of replicas that are sufficiently caught up with the leader, and it directly affects durability guarantees, leader election safety, and the behavior of `acks=all`.

## How A Replica Enters Or Leaves ISR
- Followers continuously fetch from the leader.
- If a follower stays within allowed lag, it remains in ISR.
- If it falls behind beyond time or message thresholds, the leader removes it from ISR.
- When it catches up again, it can rejoin ISR.

```mermaid
flowchart LR
    L[Leader] --> F1[Follower 1]
    L --> F2[Follower 2]
    F1 --> ISR[ISR = {Leader, F1, F2}]
    F2 --> ISR
    X[Follower lag spike] --> SHRINK[ISR shrink]
```

## Why ISR Matters
- High watermark advances only when records are replicated to the required replicas.
- `min.insync.replicas` is evaluated against current ISR size.
- Clean leader election should choose from ISR to avoid acknowledged data loss.

## Lag Measurement
- Kafka uses follower fetch progress, not just wall-clock ping health.
- A broker can be alive but still out of ISR if disk or network makes it too slow.
- Common causes of ISR shrink:
  - slow disks
  - network bottlenecks
  - GC pauses
  - overloaded leaders

## Example
Replication factor = 3  
`min.insync.replicas = 2`

State:
- Leader `B1`
- Followers `B2`, `B3`
- ISR = `{B1, B2, B3}`

If `B3` falls behind:
- ISR becomes `{B1, B2}`
- `acks=all` still succeeds

If `B2` also falls behind:
- ISR becomes `{B1}`
- producers with `acks=all` start failing with insufficient ISR errors

## Operational Implications
- Frequent ISR flapping indicates unstable broker performance.
- Under-replicated partitions are often an early warning before real availability issues.
- Large batches can increase follower catch-up time after temporary slowness.

## Tuning Notes
- Use `acks=all` with an appropriate `min.insync.replicas`.
- Do not treat replication factor alone as durability.
- Check ISR shrink and expand rates, not only snapshot ISR counts.

## Interview Angle
- ISR is about replication progress, not just replica membership.
- A partition can stay available but less durable when ISR shrinks.
- Unclean leader election allows leaders outside ISR and can trade availability for data loss risk.

## Related
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Replication-Internals.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Leader-Election.md]]
