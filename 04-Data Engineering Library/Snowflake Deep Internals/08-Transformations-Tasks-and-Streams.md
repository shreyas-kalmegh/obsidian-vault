# Transformations, Tasks, and Streams

## ELT layering model
Practical layers:
- Raw: source-aligned, minimally changed.
- Staging: cleaned and standardized.
- Mart: business-friendly dimensional or domain models.

## Streams for change tracking
Streams capture row-level change data on tables/views.

Use cases:
- Incremental transformations
- CDC-style downstream processing

Operational note:
- Streams track offsets; consumers should be designed for reliable progression.

## Tasks for scheduling
Tasks execute SQL on schedules or dependency graphs.

Patterns:
- Root task on schedule
- Child tasks for DAG-like sequencing

Guidance:
- Keep tasks focused and observable.
- Add failure alerting and retry approach externally if needed.

## Incremental transformation strategy
- Build deterministic merge keys.
- Prefer `MERGE` for upsert semantics when source updates are expected.
- Partition work by date/window for controllable backfills.

## Backfills and replay
Backfills are normal in production.

Recommendations:
- Make transformations parameterizable by date range.
- Isolate backfill compute from interactive workloads.
- Validate row counts and key metrics before publish.

## Tooling integration
Snowflake works well with dbt and orchestration tools.

Best practice:
- Keep business logic in versioned SQL models.
- Use orchestration for dependencies, retries, and environment promotion.
