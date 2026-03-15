# Pinot Star-Tree Index

## Overview
Star-tree is Pinot's pre-aggregation index for accelerating repetitive filter-plus-group-by workloads. It stores rolled-up aggregates across selected dimensions so queries can answer from precomputed summaries instead of scanning all raw rows.

## When It Helps
- Repeated dashboard queries
- Stable aggregation patterns
- High-volume fact tables with predictable drill paths

## How It Works
- Pinot chooses split dimensions and aggregated metrics.
- It builds a tree-like structure over combinations of dimension values.
- Some branches use "star" nodes that represent aggregated values across a dimension.
- At query time, Pinot can answer from these pre-aggregated nodes when predicates and group-bys align.

## Example
Suppose dashboards repeatedly ask:
- clicks by `country`, `device_type`, and hour
- filtered by `tenant_id`

Instead of scanning many raw event rows every time, a star-tree can store partial aggregates for those dimensions and metrics, dramatically reducing per-query work.

## Tradeoffs
- Faster repeated aggregations
- Extra storage and build cost
- Less benefit when query shapes vary widely

## Operational Notes
- Star-tree is powerful when you know the workload well.
- Bad dimension choices can make the index large without helping much.
- It is best for stable serving workloads, not exploratory ad hoc querying.

## Interview Angle
- Star-tree is a specialized OLAP accelerator, not a universal default.
- It trades ingestion complexity and storage for read latency.
- Pinot is especially strong when such workload-aware indexes are used well.

## Related
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Indexing-Strategies.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Scaling-Strategies.md]]
