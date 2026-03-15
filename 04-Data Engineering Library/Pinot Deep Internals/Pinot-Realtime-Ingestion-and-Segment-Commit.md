# Pinot Realtime Ingestion And Segment Commit

## Overview
Pinot realtime ingestion reads from a stream, appends records into consuming segments, then seals and commits those segments so they become immutable queryable units. Freshness depends on both stream progress and healthy segment lifecycle management.

## Core Flow
1. Realtime servers consume from stream partitions.
2. Records are appended into consuming segments.
3. Flush thresholds based on rows, time, or size trigger segment sealing.
4. A completed segment is built and committed.
5. Metadata is updated so the segment becomes available across the cluster.

## Low-Level Consumer Pattern
- A stream partition is typically owned deterministically by a server replica group.
- This reduces duplicate consumption and makes routing more predictable.
- Commit coordination matters because only one finalized segment should become authoritative for a given consumption window.

## Example
If a server is consuming from Kafka partition 3 and reaches its flush threshold:
- current in-memory consuming segment is sealed
- Pinot builds an immutable segment file
- controller metadata is updated
- a new consuming segment starts for the next offset range

## Operational Tradeoffs
- Very small flush thresholds create too many tiny segments.
- Very large thresholds reduce freshness and can increase memory pressure.
- Stream lag and segment commit lag are separate problems and should be monitored separately.

## Failure Scenarios
- Consumer stalls cause freshness lag even if queries stay healthy.
- Segment commit problems can leave data consumed but not yet broadly queryable.
- Replica ownership instability can create operational noise and recovery delays.

## Interview Angle
- Pinot realtime serving is not just "read from Kafka and query instantly"; it relies on consuming segment lifecycle and commit coordination.
- Freshness is a function of ingestion, flush policy, and metadata publication.
- Tiny realtime segments often become a scale bottleneck before raw CPU does.

## Related
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Offline-vs-Realtime-Tables.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Monitoring-KPIs.md]]
