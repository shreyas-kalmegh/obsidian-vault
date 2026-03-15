# Kubernetes Observability And KPIs

## Overview
Kubernetes monitoring should cover control-plane health, node capacity, workload health, deployment safety, and application signals. Looking at node CPU alone usually hides the real reason a platform is unstable.

## Control Plane KPIs
- API server latency and error rate
- etcd latency and health
- scheduler queue and scheduling latency
- controller reconciliation backlogs

## Node And Resource KPIs
- CPU and memory utilization
- CPU throttling
- memory pressure and OOM kills
- disk pressure
- pod density per node

## Workload KPIs
- pod restart rate
- `Pending` pod count
- probe failure rate
- rollout duration and stuck rollout count
- job success and failure rate

## Network And Service KPIs
- Service-level latency and error rate
- DNS resolution errors
- ingress response codes
- network policy drops where observable

## Example Debug Pattern
Symptoms:
- pods restarting often
- node CPU moderate
- memory OOM events rising
- rollout failures increasing

Likely causes:
- memory limits too low
- bad readiness or startup assumptions
- resource sizing mismatch rather than raw cluster CPU shortage

## Practical Dashboard Rules
- Always pair pod health with application health.
- Track requests, limits, and throttling together.
- Separate control-plane issues from workload issues.

## Interview Angle
- Kubernetes metrics are only useful when tied to object lifecycle and app behavior.
- Pod restart count is a symptom, not a root cause.
- Control-plane KPIs matter because the cluster is an API-driven control system.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Rolling-Updates-and-Probes.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Autoscaling-and-Capacity.md]]
