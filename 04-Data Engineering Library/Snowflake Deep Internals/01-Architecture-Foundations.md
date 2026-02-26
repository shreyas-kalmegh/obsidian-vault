# Architecture Foundations

## Mental model
Snowflake separates storage, compute, and cloud services:
- Storage: central persisted data layer.
- Compute: independent virtual warehouses that execute queries.
- Cloud services: metadata, optimization, auth, transaction coordination.

This separation is the core reason Snowflake scales differently than legacy MPP systems.

## Why this matters in engineering
- You can isolate workloads by assigning different warehouses.
- One team can run heavy transformations without blocking BI users, if warehouses are separated.
- Storage growth and compute scaling are managed independently.

## Database hierarchy and object model
Core hierarchy:
- Organization -> Account -> Database -> Schema -> Object (table/view/stage/task/etc.)

Operational implication:
- Use database and schema boundaries to encode ownership and lifecycle.
- Treat schemas as deployment units (for example, `raw`, `staging`, `mart`, `sandbox`).

## Transaction model (practical view)
Snowflake provides ACID transactions and multi-statement transaction support. In practice:
- Keep transactions short in ELT jobs.
- Avoid long-running open transactions that lock object metadata changes.

## Time Travel and Fail-safe
- Time Travel: query or recover data from historical snapshots for a retention period.
- Fail-safe: additional recovery period managed by Snowflake after Time Travel.

Engineering impact:
- Great for recovery and debugging accidental deletes.
- Storage cost increases with retention and frequent data modifications.

## Practical design guidelines
- Split compute by workload class early (`ETL_WH`, `BI_WH`, `DS_WH`).
- Design schema boundaries before writing transformations.
- Define naming conventions for objects to avoid metadata chaos.
