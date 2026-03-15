# Pinot Indexing Strategies

## Overview
Pinot supports multiple index types because no single index fits every analytical workload. The right strategy depends on whether queries are filter-heavy, range-heavy, text-heavy, or aggregation-heavy.

## Common Index Types
- Dictionary encoding for compact storage and fast value mapping
- Inverted index for selective equality and `IN` filters
- Range index for ordered numeric filtering
- Bloom filter for fast negative membership checks
- JSON and text indexes for semi-structured and search-like access patterns
- Star-tree for repeated aggregation workloads

## How To Choose
- Use inverted indexes on frequently filtered low-to-medium cardinality dimensions.
- Use range indexes where bounded numeric filters are common.
- Use bloom filters when point lookups on high-cardinality columns often return no match.
- Use JSON or text indexes only for workloads that really need them.

## What Not To Do
- Do not enable every index everywhere.
- Do not copy index settings from one table to another without checking query patterns.
- Do not ignore storage and build-time overhead.

## Example
A metrics table is queried by:
- `tenant_id`
- `event_time`
- `country`
- repeated group-by on `campaign_id`

Reasonable design might include:
- inverted index on `tenant_id` and `country`
- range or time-aware pruning on `event_time`
- star-tree if dashboard aggregations repeat heavily by campaign and time bucket

## Operational Notes
- Index usefulness should be validated against real query distributions.
- Wide tables with too many indexes can hurt ingestion speed and memory efficiency.
- Segment pruning often delivers more value than row-level indexes when time filters are strong.

## Interview Angle
- Pinot indexing is workload engineering, not checkbox optimization.
- The best index strategy minimizes unnecessary scans without overpaying during ingestion.
- Star-tree is not a replacement for general-purpose indexes.

## Related
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Star-Tree-Index.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Monitoring-KPIs.md]]
