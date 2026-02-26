# Callbacks and Notifiers

## Overview
Callbacks and notifiers convert task state changes into operational signals. They are essential for fast incident response and reliable ownership.

## Callback Types (Common)
- `on_success_callback`
- `on_failure_callback`
- `on_retry_callback`
- DAG-level callbacks for broader notification logic

Use callbacks for concise, actionable context. Avoid very heavy logic inside callback code.

## Example: Failure Callback

```python
from airflow.utils.context import Context

def task_failure_alert(context: Context):
    ti = context["ti"]
    msg = (
        f"[AIRFLOW] task failed | dag={ti.dag_id} "
        f"task={ti.task_id} run_id={ti.run_id} try={ti.try_number}"
    )
    print(msg)  # replace with Slack/PagerDuty notifier
```

## Notifier Design Pattern
1. Normalize event payload (dag, task, run, owner, env, severity).
2. Send through notifier abstraction (Slack/email/PagerDuty/webhook).
3. Deduplicate noisy repeats.
4. Escalate only when retry budget exhausted or SLA risk is high.

## Example: Minimal DAG-Level Integration

```python
with DAG(
    dag_id="orders_daily_pipeline",
    on_failure_callback=task_failure_alert,
    ...
):
    ...
```

## Practical Alerting Rules
- Alert on final failure, not every transient retry by default.
- Include direct runbook link in alert body.
- Include owner/team metadata for routing.
- Track notification latency as an operational metric.

## Common Mistakes
- Callback raises its own exception and hides root cause.
- Excessive retry alerts create pager fatigue.
- Missing context fields make alerts non-actionable.
- Hardcoding secret tokens inside DAG files (use Connections/Secrets backend).
