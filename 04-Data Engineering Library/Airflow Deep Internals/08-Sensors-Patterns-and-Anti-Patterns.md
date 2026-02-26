# Sensors: Patterns and Anti-Patterns

## Overview
Sensors gate workflow progress based on external readiness (file arrival, upstream DAG completion, table existence). They are useful but easy to misuse.

## Sensor Modes

1. `poke` mode
- Repeatedly checks condition while occupying a worker slot.
- Good for short waits only.

2. `reschedule` mode
- Releases worker slot between checks.
- Better for medium/long waits if deferrable option is unavailable.

3. Deferrable sensors
- Best for long waits with Triggerer support.
- Lowest worker-slot overhead.

## Example: External DAG Dependency (Reschedule)

```python
from airflow.sensors.external_task import ExternalTaskSensor

wait_publish = ExternalTaskSensor(
    task_id="wait_publish",
    external_dag_id="upstream_publish_dag",
    external_task_id="publish_done",
    mode="reschedule",
    poke_interval=300,
    timeout=2 * 60 * 60,
)
```

## Good Patterns
- Set explicit `timeout` and `poke_interval`.
- Use business-aligned SLAs for wait bounds.
- Route heavy sensor groups to dedicated pools if needed.

## Anti-Patterns
- Thousands of poke-mode sensors in small worker cluster.
- Missing timeout, causing never-ending wait loops.
- Tight polling intervals against fragile/rate-limited APIs.
- Using sensors where event-driven scheduling would be cleaner.

## Debug Checklist
1. Are sensors blocking worker slots?
2. Is wait caused by true upstream lag or wrong dependency target?
3. Are timeouts aligned with upstream schedule/SLA?
4. Is polling interval over-aggressive?

## Practical Rule
Prefer event or dataset-driven scheduling first. When sensors are required, prefer deferrable or reschedule mode over poke mode.
