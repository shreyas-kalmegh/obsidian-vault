# Medallion Architecture

## Overview
Medallion organizes data into quality layers:
- Bronze: raw, replayable ingestion
- Silver: cleaned and standardized canonical data
- Gold: business-ready dimensional/semantic models

This is a data quality and contract pattern, not just folder naming.

## Layer Contracts
### Bronze
- Keep raw payload and source metadata (`ingest_ts`, offsets, file path)
- Minimal transformations
- Immutable or append-focused for audit/replay

### Silver
- Apply schema enforcement, deduplication, and type normalization
- Handle CDC semantics and delete propagation
- Expose canonical domain entities/events

### Gold
- Build business-facing facts/dimensions and metric-ready tables
- Apply SCD policies where business history matters
- Optimize for consumption and semantic consistency

## Example Flow
- Bronze: `events_kafka_raw`
- Silver: `events_canonical`
- Gold: `fct_order_line`, `dim_customer`, `daily_country_metrics`

## Design Rules
1. Bronze should never contain business KPI logic.
2. Silver should avoid ad hoc metric definitions.
3. Gold should not bypass Silver contracts.

## Common Mistakes
- Putting dashboard-specific calculations in Silver
- Losing replay metadata in Bronze
- Rebuilding Gold from mixed Silver/Bronze logic without governance

## Practical Checklist
1. Define schema and quality rules per layer.
2. Define ownership per table and layer.
3. Automate replay/backfill from Bronze.
4. Add lineage from Bronze to Gold.

## Related Notes
- [[cdc-and-incremental-modeling]]
- [[gold-layer-dimensional-models]]
