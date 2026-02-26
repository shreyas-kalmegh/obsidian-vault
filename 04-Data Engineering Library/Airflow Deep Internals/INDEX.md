# Airflow Deep Internals - Index

Practical, medium-depth Airflow notes focused on production data platform usage and interview readiness.

## Suggested reading order
1. `01-Airflow-Architecture-Foundations.md`
2. `02-DAG-Authoring-and-Dependency-Patterns.md`
3. `03-Scheduler-Internals-and-Task-Lifecycle.md`
4. `04-Reliability-Idempotency-and-Data-Contracts.md`
5. `05-Performance-Tuning-Backfills-and-Cost.md`
6. `06-Airflow-on-Kubernetes-and-Operations.md`
7. `07-Triggerer-and-Deferrable-Execution.md`
8. `08-Sensors-Patterns-and-Anti-Patterns.md`
9. `09-Callbacks-and-Notifiers.md`
10. `10-Hooks-Connections-and-Provider-Patterns.md`
11. `11-Interview-Compact-Set.md`

## Codex session files
- `CONTEXT.md` (token-efficient working context)
- `SESSION_HANDOVER.md` (what was changed + what to do next)

## Scope
These notes cover:
- DAG orchestration for batch and micro-batch pipelines
- Scheduler/executor internals and operational behavior
- Reliability patterns for retries, backfills, and late data
- Platform operations on Kubernetes and managed Airflow setups
