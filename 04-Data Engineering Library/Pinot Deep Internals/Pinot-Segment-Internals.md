# Pinot Segment Internals

## Overview
Pinot stores data in immutable segments that contain columnar data, metadata, and optional indexes. Segment design is central because Pinot's query planner and execution model operate largely at segment granularity.

## What A Segment Contains
- Column data, often dictionary-encoded
- Segment metadata such as min/max values and row counts
- Optional indexes like inverted, range, bloom, text, JSON, or star-tree
- Forward index structures for reading stored values efficiently

## Why Segments Matter
- Queries can prune whole segments before scanning rows.
- Segments are easy to move across servers for balancing and replication.
- Immutable completed segments make serving more predictable.

## Segment Lifecycle
1. Data is ingested into a segment.
2. Segment is built with metadata and configured indexes.
3. Completed segment is published and assigned to servers.
4. Queries use segment metadata to skip or scan it.
5. Background tasks may merge, roll up, or replace segments later.

## Example
A query filters on `event_time` for the last 15 minutes. If older segments have max timestamps far below that window, Pinot can avoid scanning them entirely.

That is often the first big latency win, even before row-level indexes are considered.

## Tradeoffs
- Too many small segments increase broker routing and per-segment overhead.
- Very large segments may reduce pruning precision and increase scan cost.
- Segment design should match ingestion cadence and query patterns.

## Operational Notes
- Segment count is a critical operational metric, not just a storage detail.
- Good time partitioning often improves both retention handling and query pruning.
- Segment metadata quality strongly influences query efficiency.

## Interview Angle
- Segment is to Pinot what partitioned files or shards are to other analytics systems, but with execution-aware metadata built in.
- Pinot performance depends heavily on skipping work before scanning rows.
- Immutable segments simplify serving and indexing.

## Related
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Indexing-Strategies.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Scaling-Strategies.md]]
