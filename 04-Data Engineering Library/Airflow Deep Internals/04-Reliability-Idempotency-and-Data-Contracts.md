# Reliability, Idempotency, and Data Contracts

## Overview
Airflow reliability is mostly about task design, not just retries. Orchestration retries only work safely when underlying operations are idempotent and bounded by clear data contracts.

## Idempotency Patterns

1. Partition-overwrite by run date
- Write to deterministic partition path/table slice (`ds`/`data_interval_start`).

2. MERGE/UPSERT with stable business keys
- Avoid duplicate inserts when retries happen.

3. External side effects with de-dup keys
- Use operation IDs so repeated calls do not duplicate work.

## Example: Idempotent Warehouse Load (SQL pattern)

```sql
MERGE INTO analytics.orders t
USING staging.orders_delta s
ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET
  status = s.status,
  updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (
  order_id, status, updated_at
) VALUES (
  s.order_id, s.status, s.updated_at
);
```

Why this is retry-safe:
- Re-running same source window converges to same final target state.

## Data Contracts in DAGs
- Define expected schema, partition completeness, and freshness SLA.
- Validate contract before publish/consume handoff.
- Fail fast on hard contract breaks; do not silently proceed.

## Late Data and Backfills

Recommended approach:
1. Use interval-aware processing (`data_interval_start/end`).
2. Build bounded replay windows (for example, last 7 days).
3. Separate routine schedule from historical backfill workloads.

## Failure Taxonomy (Useful in Incidents)
- Transient infra failure: retry with backoff.
- Deterministic code/data bug: fail quickly and alert.
- External dependency outage: circuit-break with controlled retries.
- Contract/schema break: stop downstream publish.

## Practical Callbacks
- Use `on_failure_callback` to emit concise incident context:
  - DAG/task/run ID
  - upstream/downstream impact
  - retry count and last error class

## Common Reliability Mistakes
- Using retries without idempotent writes.
- Mixing control-plane metadata and data-plane payloads in XCom.
- Running massive historical backfills with normal prod concurrency limits.
- No guardrails for schema drift.
