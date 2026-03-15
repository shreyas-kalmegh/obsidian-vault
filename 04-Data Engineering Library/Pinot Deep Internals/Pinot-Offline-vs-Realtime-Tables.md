# Pinot Offline Vs Realtime Tables

## Overview
Pinot exposes two main ingestion models: offline tables for batch-loaded data and realtime tables for streamed data. A hybrid table combines both to deliver historical depth plus fresh results through one logical query surface.

## Offline Tables
- Built from batch ingestion jobs.
- Good for large historical backfills and predictable segment generation.
- Often easier to optimize because segments are immutable before serving.

## Realtime Tables
- Ingest from streams such as Kafka.
- Data lands in consuming segments and later becomes completed immutable segments.
- Designed for freshness, but comes with stream-consumption and commit complexity.

## Hybrid Tables
- Pair one offline table with one realtime table for the same dataset.
- Brokers merge results from both sides.
- Time boundaries help avoid double counting or gaps.

## Example
Suppose product analytics data is batch-loaded nightly for the past 90 days, while the current day is ingested from Kafka.

Possible layout:
- offline table: days `T-90` to `T-1`
- realtime table: current day
- broker query: merges both for a dashboard covering last 30 days

## Tradeoffs
- Offline is easier to bulk optimize and compact.
- Realtime gives freshness but increases operational moving parts.
- Hybrid improves usability, but boundary management must be correct.

## Operational Notes
- Hybrid overlap bugs can create duplicate counts if offline and realtime windows are not coordinated.
- Realtime tables benefit from careful flush thresholds so segments are not too tiny or too large.
- If freshness is not needed, pure offline tables are often simpler and cheaper.

## Interview Angle
- Hybrid tables are a query-serving abstraction over offline plus realtime storage, not a third storage type.
- Realtime tables are about freshness, not necessarily lower cost.
- Pinot often shines when users want warehouse-like analytics with serving-layer latency.

## Related
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Realtime-Ingestion-and-Segment-Commit.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Query-Routing-and-Execution.md]]
