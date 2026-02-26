# Airflow on Kubernetes and Operations

## Overview
Kubernetes gives strong isolation and elastic operations for Airflow, but introduces cluster-level failure modes (pod scheduling, image pulls, node pressure, RBAC/network policies).

## Common K8s Deployment Shapes

1. CeleryExecutor on K8s
- Scheduler + webserver + workers as deployments.
- Broker (Redis/RabbitMQ) + metadata DB required.

2. KubernetesExecutor
- Scheduler creates short-lived pods per task.
- Strong isolation; higher pod scheduling overhead.

## KubernetesExecutor Mental Model
- Each task instance can become a pod.
- Pod startup latency matters for short tasks.
- Image size and pull behavior directly impact DAG latency.

## Example: Task-Level Pod Override

```python
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

run_job = KubernetesPodOperator(
    task_id="run_transform",
    name="run-transform",
    namespace="airflow",
    image="ghcr.io/acme/data-jobs:2025-02-15",
    cmds=["python", "jobs/transform.py"],
    get_logs=True,
    is_delete_operator_pod=True,
)
```

## Operational Runbook (Compact)

If tasks remain queued:
1. Check scheduler heartbeat.
2. Check executor queue and worker/pod capacity.
3. Check pool exhaustion.
4. Check metadata DB saturation.

If tasks fail fast on K8s:
1. Inspect pod events (`ImagePullBackOff`, `OOMKilled`, `Unschedulable`).
2. Verify service account/RBAC and secrets mounts.
3. Verify network policies to DB/warehouse/API endpoints.

If retries spike:
1. Classify by error class (infra vs deterministic code).
2. Check upstream dependency health.
3. Reduce concurrency if downstream is throttling.

## CI/CD and Change Safety
- Version DAGs and dependencies together.
- Use canary DAG or limited schedule for risky rollout.
- Rollback path should be simple:
  - revert DAG code
  - revert image tag
  - clear affected task instances only if needed

## SLO Suggestions
- Scheduler health SLO (heartbeat and parse delay)
- DAG completion SLO (on-time success rate)
- Alert latency SLO (time from failure to notification)

## Common Ops Mistakes
- No resource requests/limits for scheduler/webserver/workers.
- Very large container images causing startup lag.
- Shared queues/pools across unrelated critical workloads.
- Missing on-call runbooks for recurrent failure patterns.
