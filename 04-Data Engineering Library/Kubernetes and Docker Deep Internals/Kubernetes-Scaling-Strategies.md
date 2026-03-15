# Kubernetes Scaling Strategies

## Overview
Scaling Kubernetes is about balancing workload shape, replica count, node capacity, scheduling policy, and operational overhead. More nodes or pods help only if the application and cluster constraints allow the extra capacity to be used effectively.

## Common Scaling Levers
- Add pod replicas for stateless workloads
- Add nodes for more cluster capacity
- Tune requests and limits for better packing
- Split noisy or critical workloads across node pools
- Use autoscaling carefully with realistic metrics

## Workload Scaling
- Stateless APIs usually scale horizontally most easily.
- Stateful systems often need partition-aware or shard-aware scaling.
- Batch workloads may compete badly with latency-sensitive services if pools are shared carelessly.

## Cluster Scaling
- Bigger clusters increase scheduling and operational complexity.
- Overly small nodes can increase scheduling fragmentation.
- Overly large nodes can increase blast radius and noisy-neighbor effects.

## Example
A team doubles node count, but throughput barely improves.

Possible reasons:
- app is bottlenecked by a database
- resource requests still prevent good placement
- Service or ingress layer is saturated
- the workload is stateful and cannot scale linearly

## Operational Notes
- Scaling policy should reflect application architecture, not just cluster features.
- Request sizing is a first-class scaling control.
- Node pool specialization is often cleaner than one giant undifferentiated cluster.

## Interview Angle
- Kubernetes scales infrastructure and replicas, not arbitrary application bottlenecks.
- Good scaling strategy includes scheduling, disruption control, and dependency awareness.
- Capacity efficiency and reliability often pull in opposite directions.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Autoscaling-and-Capacity.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Observability-and-KPIs.md]]
