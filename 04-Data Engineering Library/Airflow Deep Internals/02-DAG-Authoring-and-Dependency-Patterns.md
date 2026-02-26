# DAG Authoring and Dependency Patterns

## Overview
Good DAG authoring balances clarity, reliability, and scheduler efficiency. The main production goal is stable, rerunnable workflows with predictable dependencies.

## TaskFlow vs Traditional Operators

TaskFlow (`@task`) strengths:
- Pythonic dependency wiring.
- Strong readability for ETL-style DAGs.
- Easy passing of small metadata via XCom.

Traditional operators strengths:
- Better for provider integrations and explicit templated fields.
- Useful when teams already use standard operator sets.

## Example: Dynamic Task Mapping
Use mapping when fan-out count depends on runtime data.

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(start_date=datetime(2025, 1, 1), schedule="@daily", catchup=False)
def ingest_partitions():
    @task
    def discover_partitions():
        return ["us", "eu", "apac"]

    @task
    def ingest_region(region: str):
        print(f"ingest region={region}")

    ingest_region.expand(region=discover_partitions())

ingest_partitions()
```

Tradeoff:
- Mapping increases task instance count; enforce limits with pools/concurrency.

## Sensors: Avoid Slot Waste
Long-wait sensors in poke mode can starve workers.

Better pattern:
- Prefer deferrable sensors/operators when available.
- Or use `mode="reschedule"` for classic sensors.

```python
from airflow.sensors.external_task import ExternalTaskSensor

wait_upstream = ExternalTaskSensor(
    task_id="wait_upstream",
    external_dag_id="upstream_dag",
    external_task_id="publish_done",
    mode="reschedule",
    timeout=3600,
)
```

## Dependency Patterns

1. Linear ETL chain
- `extract >> transform >> load`
- Good for simple daily batches.

2. Fan-out/Fan-in
- One producer, many parallel consumers, one final aggregate.
- Add safeguards for partial failures and retries.

3. Dataset/event-driven dependencies
- Better than time-only coupling for cross-DAG dependencies.
- Use when downstream should run only after specific upstream data is ready.

## XCom Usage Rule
- Use XCom for small control-plane payloads (IDs, paths, counts).
- Do not put large dataframes/blobs in XCom.
- Store large outputs externally (S3/GCS/warehouse), pass references.

## Common Authoring Mistakes
- Non-deterministic DAG definitions (runtime API calls during parse).
- Very large single-task code blobs with no isolation boundaries.
- Missing retry/idempotency assumptions.
- Excessive task explosion from unbounded dynamic mapping.

## Checklist
- Are tasks idempotent?
- Is fan-out bounded?
- Are long waits deferrable/rescheduled?
- Is XCom payload small?
- Can a failed run be replayed safely?
