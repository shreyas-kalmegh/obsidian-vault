# Airflow Architecture Foundations

## Overview
Airflow is an orchestration system, not a compute engine. It schedules and tracks tasks, while actual compute runs in external systems (Spark, dbt, warehouses, Python jobs, APIs).

Core idea:
- Model workflow as a DAG.
- Schedule DAG runs.
- Execute tasks with an executor.
- Persist state in metadata DB.

## Core Components

1. Scheduler
- Parses DAG files and creates runnable task instances.
- Applies dependencies, pools, priorities, concurrency limits.

2. Webserver
- UI for DAGs, task states, logs, retries, and manual operations.

3. Executor
- Decides where tasks actually run.
- Common options: `LocalExecutor`, `CeleryExecutor`, `KubernetesExecutor`.

4. Metadata Database
- Source of truth for DAG run/task instance states and scheduler bookkeeping.
- Usually PostgreSQL/MySQL in production.

5. Triggerer (for deferrable operators)
- Handles async waiting to reduce worker slot usage for long waits/sensors.

## Execution Flow (Simplified)
1. DAG file is parsed and serialized.
2. Scheduler creates `DagRun` and `TaskInstance` rows.
3. Runnable tasks are queued to executor.
4. Workers execute task code and update status.
5. Scheduler advances downstream tasks until terminal DAG state.

## Example: Minimal Production DAG Skeleton

```python
from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta

with DAG(
    dag_id="orders_daily_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["orders", "prod"],
) as dag:

    @task
    def extract():
        return "s3://raw/orders/dt={{ ds }}"

    @task
    def transform(path: str):
        return f"transformed:{path}"

    @task
    def load(result: str):
        print(result)

    load(transform(extract()))
```

Why this pattern works:
- Small, testable tasks.
- Explicit retries and run concurrency.
- Clear flow from extract to load.

## Common Architecture Mistakes
- Treating Airflow as a compute cluster instead of orchestration control-plane.
- Running very heavy Python processing inside scheduler/worker process without external engines.
- Using SQLite metadata DB outside local development.
- High-frequency polling sensors that consume worker slots.

## Practical Guidance
- Keep metadata DB healthy first; scheduler correctness depends on it.
- Use deferrable operators for long waits.
- Set DAG-level concurrency intentionally (`max_active_runs`, task limits, pools).
- Make external jobs idempotent; retries are normal in distributed systems.
