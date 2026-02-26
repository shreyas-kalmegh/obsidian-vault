# Scheduler Internals and Task Lifecycle

## Overview
Most production Airflow issues are scheduler-state issues: parsing bottlenecks, queueing delays, or concurrency constraints. Understanding lifecycle states is key to debugging.

## Parse to Execute Path
1. Scheduler parses DAG files from `dags_folder`.
2. DAGs are serialized and metadata is refreshed.
3. Scheduler creates `DagRun` and `TaskInstance` records.
4. Runnable tasks are selected based on dependencies + limits.
5. Tasks are queued and executed via executor/workers.

## Task Instance State Model (Common)
- `none` -> not yet considered
- `scheduled` -> dependencies satisfied
- `queued` -> sent to executor queue
- `running` -> currently executing
- `success` / `failed` / `up_for_retry` / `skipped`

Why this matters:
- Delays between `scheduled` and `queued` usually mean scheduler/concurrency bottleneck.
- Delays between `queued` and `running` usually mean executor/worker capacity issue.

## Concurrency Controls (Most Important)

1. DAG-level:
- `max_active_runs`
- `max_active_tasks` (or DAG/task concurrency settings depending on version)

2. Global:
- `parallelism`
- `max_active_tasks_per_dag` (environment-level guard)

3. Pool-level:
- Pool slots to protect shared systems (warehouse/API).

4. Task-level:
- Priority weight and queue routing.

## Example: Pool-Protected External API

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def call_rate_limited_api():
    pass

with DAG(
    "api_ingest",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
) as dag:
    PythonOperator(
        task_id="pull_api",
        python_callable=call_rate_limited_api,
        pool="partner_api_pool",  # pool size managed in Airflow UI/CLI
        retries=3,
    )
```

## Retry Lifecycle and Failure Semantics
- Failure does not imply bad DAG design by itself.
- Retries are expected for transient errors (network, temporary locks, API 5xx).
- Retry policy should reflect source behavior.

Recommended defaults:
- Bounded retries
- Exponential backoff for flaky dependencies
- Failure callback for high-value pipelines

## Debugging Playbook
1. Check DAG run graph: where did progress stop?
2. Check task state transition timing (`scheduled -> queued -> running`).
3. Check pools and executor queue depth.
4. Check worker logs and external system errors.
5. Verify metadata DB health/latency and scheduler heartbeat.

## Common Pitfalls
- Too many DAG files and expensive top-level imports slowing parse.
- Unbounded backfills overwhelming scheduler.
- Misconfigured pools causing hidden queue starvation.
- Overly permissive concurrency causing downstream system overload.
