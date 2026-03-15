# Kubernetes Interview Questions For Data Engineering

## How To Use This Note
- Aim for concise systems-oriented answers.
- Tie concepts to batch jobs, streaming systems, stateful services, and production reliability.
- Prefer tradeoffs and failure modes over definitions alone.

## Core Questions
### 1. What is the relationship between Docker and Kubernetes?
Docker packages applications into containers and runs them locally or on hosts. Kubernetes orchestrates containers across a cluster by scheduling, networking, scaling, and replacing them automatically.

### 2. What is a pod and why does Kubernetes use it instead of scheduling individual containers?
A pod is the smallest deployable unit in Kubernetes and can hold one or more tightly coupled containers that share network namespace and volumes. Kubernetes schedules pods because sidecars and helper containers often need to live and fail together.

### 3. What does the Kubernetes control plane do?
The control plane stores desired state, accepts API updates, schedules pods, and runs controllers that reconcile actual cluster state toward the declared configuration.

### 4. What is a Deployment?
A Deployment manages stateless replicated pods through ReplicaSets. It supports rolling updates, rollbacks, and declarative replica management.

### 5. What is the difference between Deployment and StatefulSet?
- Deployment is for interchangeable stateless replicas.
- StatefulSet gives stable identity, ordered rollout behavior, and persistent volume attachment patterns for stateful workloads.

### 6. What is a Service?
A Service provides a stable virtual IP and DNS name for a dynamic set of pods selected by labels. It decouples clients from pod churn.

### 7. Why do pods get replaced instead of repaired in place?
Kubernetes treats pods as replaceable units. Controllers create new pods to restore desired state because that model is simpler and more reliable than trying to repair arbitrary runtime drift.

### 8. What is the difference between requests and limits?
- Requests influence scheduling and reserved capacity assumptions.
- Limits cap runtime resource usage.

If limits are set too tightly, CPU throttling or OOM kills can hurt stability.

### 9. When would a data engineering system use StatefulSets?
For systems that need stable network identity or persistent storage attachment, such as Kafka brokers, ZooKeeper-like systems, or some databases.

### 10. Why is Kubernetes useful for data engineering platforms?
It standardizes deployment, autoscaling, service discovery, and self-healing for batch jobs, stream processors, APIs, and platform components across environments.

## Scenario Questions
### 11. A pod is stuck in `Pending`. What would you check?
- insufficient node resources
- unsatisfied node selectors or affinity rules
- taints and tolerations mismatch
- PVC not bound
- namespace quota or limit range issues

### 12. A Deployment rollout is stuck. What does that suggest?
Likely readiness probe failures, image pull issues, bad startup config, or too-strict update settings like unavailable and surge constraints.

### 13. A Spark or Flink workload works locally in Docker but fails in Kubernetes. Why?
Possible reasons:
- wrong service discovery assumptions
- missing config or secrets
- storage differences
- resource requests too low
- container image not built for cluster execution environment

### 14. Why might autoscaling fail to improve latency?
Possible reasons:
- bottleneck is downstream database or queue
- scale-up is too slow
- requests are wrong so scheduler placement stays poor
- per-pod concurrency is saturated in a non-CPU dimension like memory or network

### 15. Why can a Service be healthy while requests still fail?
Because the problem may be in ingress routing, DNS, network policy, TLS termination, or application-level readiness rather than the Service object itself.

## Strong Follow-Up Points
- Mention reconciliation when discussing control plane behavior.
- Mention readiness versus liveness when discussing rollouts.
- Mention persistent volumes when discussing stateful systems.
- Mention resource requests and limits when discussing cluster efficiency.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-and-Docker-Cheatsheet.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Architecture.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Storage-PVs-PVCs-and-StatefulSets.md]]
