# Kubernetes And Docker Deep Internals Index

## How To Use This Index
Read these notes in order if you want a clean mental model from container fundamentals to Kubernetes control-plane behavior, workload execution, networking, storage, scaling, and production operations. The sequence starts with Docker because Kubernetes makes more sense once container primitives are clear.

## Recommended Reading Order
### Phase 1: Container Foundations
1. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Docker-Container-Runtime-Basics.md]]
2. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Docker-Image-Layers-and-Union-Filesystems.md]]
3. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Docker-Networking-and-Storage.md]]

Why first:
- These explain what containers really are, how images are built, and how networking and persistence work before Kubernetes orchestrates them.

### Phase 2: Kubernetes Core Architecture
4. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Architecture.md]]
5. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Pod-Lifecycle.md]]
6. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Controllers-and-Reconciliation.md]]

Why next:
- This layer explains the API-driven control model, the pod as the basic execution unit, and the reconciliation loops that keep desired and actual state aligned.

### Phase 3: Scheduling, Networking, And Service Discovery
7. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Scheduler-and-Placement.md]]
8. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Networking-Services-and-Ingress.md]]
9. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-DNS-and-Service-Discovery.md]]

Why here:
- Once pods and controllers are clear, it becomes easier to understand how workloads land on nodes and how traffic reaches them.

### Phase 4: State, Security, And Scaling
10. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Storage-PVs-PVCs-and-StatefulSets.md]]
11. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-ConfigMaps-Secrets-and-Security-Context.md]]
12. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Autoscaling-and-Capacity.md]]

Why next:
- These topics explain how Kubernetes handles persistent workloads, configuration, security boundaries, and growth under load.

### Phase 5: Reliability, Operations, And Interviews
13. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Rolling-Updates-and-Probes.md]]
14. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Observability-and-KPIs.md]]
15. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Scaling-Strategies.md]]
16. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Interview-Questions-Data-Engineering.md]]

Why last:
- These depend on understanding the runtime, control loops, and traffic model first.

## Fast-Track Paths
### For Data Engineering Interviews
1. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-and-Docker-Cheatsheet.md]]
2. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Docker-Container-Runtime-Basics.md]]
3. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Architecture.md]]
4. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Pod-Lifecycle.md]]
5. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Networking-Services-and-Ingress.md]]
6. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Storage-PVs-PVCs-and-StatefulSets.md]]
7. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Interview-Questions-Data-Engineering.md]]

### For Production Debugging
1. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Observability-and-KPIs.md]]
2. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Pod-Lifecycle.md]]
3. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Controllers-and-Reconciliation.md]]
4. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Networking-Services-and-Ingress.md]]
5. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Rolling-Updates-and-Probes.md]]
6. [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Autoscaling-and-Capacity.md]]

## Companion Notes
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-and-Docker-Cheatsheet.md]] for quick recall
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Interview-Questions-Data-Engineering.md]] for DE-focused interview preparation
