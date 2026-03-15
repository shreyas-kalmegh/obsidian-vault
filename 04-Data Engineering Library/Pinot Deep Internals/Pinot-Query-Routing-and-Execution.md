# Pinot Query Routing And Execution

## Overview
Pinot uses a scatter-gather query model. Brokers parse the query, determine which segments are relevant, route sub-queries to servers, and merge partial results into the final response.

## Query Path
1. Client sends SQL query to a broker.
2. Broker identifies target tables and candidate segments.
3. Broker prunes segments using metadata where possible.
4. Broker fans the query out to relevant servers.
5. Servers scan and aggregate locally.
6. Broker reduces partial results and returns the answer.

## Why Routing Quality Matters
- Good routing reduces fan-out and tail latency.
- Bad routing means too many servers participate, even for selective queries.
- Segment locality and balanced assignment affect both latency and cluster fairness.

## Segment Pruning Layers
- Table and time-range pruning
- Segment metadata pruning
- Index-assisted row pruning inside segments

## Example
A dashboard query asks for the last 10 minutes of metrics for one tenant.

Efficient path:
- broker keeps only recent segments
- tenant filter uses segment metadata or indexes
- only a small subset of servers scans rows

Inefficient path:
- all recent segments across all tenants are scanned
- broker fan-out grows
- p95 latency rises even if each server is only moderately loaded

## Operational Notes
- Tail latency often comes from the slowest participating server, not the average one.
- Query logs are useful only when paired with routing and segment statistics.
- Projection pruning matters too; selecting many wide columns can dominate scan cost.

## Interview Angle
- Pinot wins by reducing the amount of data each query has to touch.
- Broker routing is part of the execution engine, not a thin proxy layer.
- Fast OLAP in Pinot is usually "scan less, merge less" rather than "compute harder."

## Related
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Indexing-Strategies.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Multi-Stage-Query-Engine.md]]
