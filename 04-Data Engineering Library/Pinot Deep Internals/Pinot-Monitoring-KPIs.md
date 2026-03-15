# Pinot Monitoring KPIs

## Overview
Pinot monitoring should cover query latency, freshness, segment health, cluster balance, and memory pressure. Looking at CPU alone usually misses the real reason a user-facing analytics workload is slow.

## Query KPIs
- p50, p95, and p99 query latency
- queries per second
- timeout rate
- fan-out breadth by query
- scanned documents, scanned segments, and pruned segments

## Ingestion KPIs
- stream consumer lag
- realtime freshness delay
- segment flush rate
- segment commit latency
- failed or stuck ingestion tasks

## Storage And Segment KPIs
- segment count by table
- average segment size
- segment load failures
- segment replication balance
- deep-store or segment-download errors where applicable

## Resource KPIs
- server heap and GC behavior
- off-heap or mmap pressure depending on deployment model
- broker CPU and request queue pressure
- disk usage and file descriptor health

## Background Maintenance KPIs
- minion task backlog
- merge-rollup task success rate
- retention or purge task lag
- segment replacement timing

## Example Debug Pattern
Symptoms:
- p95 query latency rising
- server CPU moderate
- scanned segments very high
- freshness healthy

Likely causes:
- poor segment pruning
- missing indexes
- segment count explosion

If freshness is degrading while query latency stays flat, look first at stream lag, flush thresholds, and segment commit behavior.

## Practical Dashboard Rules
- Always pair latency with scan volume.
- Track segment counts and query fan-out over time.
- Separate freshness problems from query-serving problems.

## Interview Angle
- In Pinot, "how much data was scanned" is often more useful than CPU alone.
- Freshness is its own production SLO for realtime tables.
- Segment count is a first-class capacity metric.

## Related
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Realtime-Ingestion-and-Segment-Commit.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Scaling-Strategies.md]]
