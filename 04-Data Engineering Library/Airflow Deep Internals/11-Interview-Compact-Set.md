# Airflow Interview Compact Set

Use this for quick revision. Keep answers structured: architecture -> failure mode -> mitigation -> tradeoff.

## 1) What is Airflow and what is it not?
- Airflow is a workflow orchestrator for scheduling and dependency management.
- It is not a distributed compute engine; heavy compute should run in external systems.

## 2) Explain core components.
- Scheduler: decides what runs next.
- Executor/workers: run tasks.
- Metadata DB: stores state and orchestration metadata.
- Webserver: UI and operational controls.
- Triggerer: supports deferrable async waits.

## 3) How does task lifecycle work?
- `scheduled -> queued -> running -> success/failed/up_for_retry`.
- Long `scheduled` usually means dependency/concurrency gate.
- Long `queued` usually means executor capacity bottleneck.

## 4) How do you design idempotent tasks?
- Deterministic write targets (partition/date keyed).
- Use MERGE/UPSERT or dedup keys.
- Keep retries safe by avoiding non-idempotent side effects.

## 5) When should you use pools?
- To protect rate-limited APIs/warehouses and control shared resource contention.
- Pools enforce fairness and prevent noisy-neighbor overload.

## 6) How do you handle backfills safely?
- Separate queue/pool from daily production runs.
- Limit active runs and process in bounded windows.
- Validate sample windows before full historical replay.

## 7) Why can scheduler performance degrade?
- Heavy DAG parse-time imports/calls.
- Too many DAGs with expensive dynamic generation.
- Metadata DB latency/locking issues.

## 8) How do you reduce sensor cost?
- Use deferrable operators or `mode="reschedule"`.
- Avoid long poke-mode sensors consuming worker slots.

## 9) CeleryExecutor vs KubernetesExecutor?
- Celery: stable queue-based workers, good for steady workloads.
- KubernetesExecutor: per-task isolation/elasticity, more pod overhead.
- Choose based on workload shape and platform maturity.

## 10) What are top production metrics?
- Queue wait time (`scheduled -> running`)
- Task runtime percentiles (`p50/p95`)
- Retry/failure rate by dependency
- Scheduler heartbeat and parse delay

## 11) Common failure classes?
- Transient infra/network failures: retry/backoff.
- Deterministic code/schema issues: fail fast and fix.
- External throttling/outage: reduce concurrency, circuit-break.

## 12) How do you approach an SLA miss incident?
1. Identify where latency accumulated (queue wait vs run time).
2. Check pools/concurrency/executor capacity.
3. Inspect error concentration by dependency.
4. Mitigate quickly (throttle backfill, rebalance pools, rerun impacted windows).

## 13) What should not go into XCom?
- Large payloads (dataframes/files/blobs).
- Keep XCom for small control metadata; pass object storage references instead.

## 14) What changes are risky in Airflow?
- Concurrency changes, schedule frequency changes, retries/timeouts, executor switches.
- Roll out with canary DAGs and explicit rollback steps.

## 15) One strong interview close
"I treat Airflow as a control-plane system: reliability comes from idempotent tasks, bounded concurrency, and clear runbooks more than from aggressive config tuning."

## 16) What is the Triggerer and why does it matter?
- Triggerer powers deferrable tasks by monitoring async wait conditions.
- It releases worker slots during long waits, improving throughput and reducing cost.

## 17) Poke vs reschedule vs deferrable sensors?
- Poke: simplest, but holds worker slot.
- Reschedule: frees slot between checks, good fallback.
- Deferrable: best long-wait option when provider support exists.

## 18) How would you design callback notifications?
- Include run identity (`dag_id`, `task_id`, `run_id`, try number), error class, and runbook link.
- Alert strongly on final failure/SLA risk; suppress noisy transient retry spam.

## 19) What are hooks in Airflow?
- Hooks are provider clients used by operators/tasks to talk to external systems.
- They use `conn_id`/Connections for secure config and secret separation from DAG code.
