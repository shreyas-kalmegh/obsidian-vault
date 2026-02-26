# Triggerer and Deferrable Execution

## Overview
The Triggerer is an async component that allows long-wait tasks to pause without occupying a worker slot. This is critical for cost and throughput when many tasks mostly wait on external events.

## Why It Exists
Without deferrable execution:
- A sensor/operator in waiting state can hold a worker slot for minutes or hours.
- Worker pools become saturated with "idle waiting" tasks.

With deferrable execution:
- Task defers and state is tracked by Triggerer.
- Worker slot is released until event is ready.
- Task resumes on worker only for final execution step.

## Lifecycle (Simplified)
1. Task starts on worker.
2. Task calls `defer(...)` with trigger condition.
3. Triggerer monitors event asynchronously.
4. On event, task is rescheduled and resumes.
5. Task finishes as `success` or `failed`.

## Example: Deferrable Operator Pattern

```python
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

wait_file = S3KeySensor(
    task_id="wait_input_file",
    bucket_name="raw-zone",
    bucket_key="orders/dt={{ ds }}/_SUCCESS",
    deferrable=True,
    timeout=60 * 60,
)
```

## Operational Considerations
- Run Triggerer as a first-class production service.
- Monitor trigger backlog and Triggerer heartbeats.
- Validate provider/operator supports `deferrable=True`.

## Common Pitfalls
- Assuming every sensor/operator is deferrable.
- Running without Triggerer but enabling deferrable tasks.
- Ignoring timeout semantics (deferred task can still fail on timeout).

## Practical Rule
Use deferrable mode by default for long waits. Keep non-deferrable mode for short checks or when provider support is missing.
