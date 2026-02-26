# Virtual Warehouses and Concurrency

## Warehouse sizing strategy
Snowflake warehouse sizes scale compute resources. Larger is not always better.

Baseline approach:
- Start with a medium size for ETL and small/medium for BI.
- Measure queueing, runtime, and credit usage.
- Adjust size or split workload based on evidence.

## Concurrency and queueing
When concurrent demand exceeds available slots, queries queue.

Symptoms:
- Dashboard latency spikes during ETL windows.
- High wait time despite short actual execution.

Fix options:
- Use dedicated BI warehouse.
- Enable multi-cluster warehouse for bursty concurrent workloads.
- Stagger heavy transformations.

## Multi-cluster warehouses
Useful for concurrency, not always for single-query speed.

When to use:
- Many short concurrent BI queries.
- Traffic with predictable spikes.

When not to use:
- Single long-running batch jobs where bigger single-cluster size may be better.

## Auto-suspend and auto-resume
- Auto-resume should almost always be on.
- Auto-suspend should be short enough to control idle burn, but not so short that it thrashes start/stop cycles.

Typical pattern:
- BI: 5-10 minutes
- Scheduled ETL: 1-5 minutes depending on cadence

## Workload isolation patterns
Recommended dedicated warehouses:
- `WH_INGEST` for COPY/Snowpipe-heavy loads
- `WH_TRANSFORM` for dbt/ELT models
- `WH_BI` for dashboards
- `WH_DS` for exploratory data science

This isolation improves predictability and simplifies cost ownership.
