# Kubernetes Scheduler And Placement

## Overview
The scheduler decides where unscheduled pods should run based on resource requests, constraints, policies, and node conditions. Good placement affects performance, reliability, and cost far more than many teams expect.

## What The Scheduler Considers
- CPU and memory requests
- node selectors and affinity rules
- taints and tolerations
- topology spread constraints
- volume locality and binding constraints

## Example
If a pod requests 8 CPU but all nodes have only 4 CPU free, it stays `Pending` even if real usage would have been low. Kubernetes schedules against requests, not optimism.

## Placement Tradeoffs
- Packing improves utilization but can increase blast radius.
- Spreading improves resilience but may reduce bin-packing efficiency.
- Strict affinity rules make placement predictable but can reduce schedulability.

## Operational Notes
- Bad resource requests distort the entire cluster.
- Many `Pending` pods are policy or storage problems, not raw compute shortages.
- Topology-aware placement matters for stateful and latency-sensitive systems.

## Interview Angle
- Scheduling is driven by requested resources, not current observed usage alone.
- Affinity, anti-affinity, and taints are policy controls, not performance hacks by themselves.
- Poor placement decisions can look like app instability.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Autoscaling-and-Capacity.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Storage-PVs-PVCs-and-StatefulSets.md]]
