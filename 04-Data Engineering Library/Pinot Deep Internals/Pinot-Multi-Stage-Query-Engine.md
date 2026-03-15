# Pinot Multi-Stage Query Engine

## Overview
Pinot historically served many queries through a broker-led scatter-gather model, but more complex distributed queries benefit from a multi-stage engine. Multi-stage execution breaks a query into stages that can exchange intermediate results across workers.

## Why It Exists
- Better support for joins
- More flexible distributed execution plans
- Clearer separation between local operators and exchange stages

## Mental Model
- Stage 1 workers may scan and filter local segments.
- Intermediate results are shuffled or exchanged.
- Downstream stages perform joins, aggregations, or final reductions.

## Example
Suppose a query joins click events with a small dimension-style table and then aggregates by campaign.

Single-stage execution may be awkward or limited.
Multi-stage execution can:
- scan source tables
- repartition on join keys
- execute join logic
- aggregate final campaign metrics

## Tradeoffs
- More capable execution plans
- More network exchange overhead
- More moving parts to debug than simple scatter-gather queries

## Operational Notes
- Not every query benefits from multi-stage execution.
- Exchange-heavy plans can shift the bottleneck from scanning to network and shuffle cost.
- Capacity planning should consider both scan pressure and intermediate result movement.

## Interview Angle
- Multi-stage execution expands Pinot's query flexibility, especially for distributed relational-style operations.
- It does not remove the importance of segment pruning and local indexes.
- Complex queries can still be limited by data movement, not just CPU.

## Related
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Query-Routing-and-Execution.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Scaling-Strategies.md]]
