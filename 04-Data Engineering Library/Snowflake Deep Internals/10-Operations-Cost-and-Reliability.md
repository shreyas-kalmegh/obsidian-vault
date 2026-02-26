# Operations, Cost, and Reliability

## Cost control fundamentals
Snowflake cost is mostly driven by:
- Compute credits (warehouse runtime)
- Storage (including retained history)
- Additional services (feature-dependent)

## FinOps operating model
- Tag warehouses and major objects by team/project.
- Set resource monitors with alert thresholds.
- Review top expensive queries and idle warehouse time weekly.

## Warehouse cost patterns
Frequent waste patterns:
- Oversized warehouse for small ad hoc queries
- Long auto-suspend thresholds causing idle burn
- Shared warehouse contention causing scale-up instead of isolation

## Reliability engineering for data pipelines
- Define SLOs for freshness and pipeline success rates.
- Add observability on task history, query failures, and ingestion lag.
- Implement replay/backfill procedures before incidents happen.

## Incident response checklist
1. Identify scope (which tables/reports affected).
2. Check ingestion first, then transformation dependencies.
3. Validate warehouse health and queueing.
4. Run targeted backfill/reprocessing.
5. Record root cause and prevention action.

## Environment strategy
Use separate environments (dev/test/prod) with controlled promotion.

Guidance:
- Keep grants and core DDL version-controlled.
- Use automated checks for model quality before prod deploys.
- Restrict direct prod writes to approved pipelines.
