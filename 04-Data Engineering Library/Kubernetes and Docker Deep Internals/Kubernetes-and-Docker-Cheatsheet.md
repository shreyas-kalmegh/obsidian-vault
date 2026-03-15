# Kubernetes And Docker Deep Internals Cheatsheet

## Core Mental Model
- Docker packages and runs applications as isolated containers built from layered images.
- Kubernetes schedules those containers as pods across a cluster and continuously reconciles actual state toward desired state.
- Pods are ephemeral, but Kubernetes objects and controllers provide stable deployment behavior.
- Most production issues are not "Kubernetes is broken" but mismatches between workload design, resource limits, networking, or storage assumptions.

## Docker Quick Lookup
| Topic | Key Point |
| --- | --- |
| Image | Read-only layered filesystem plus metadata |
| Container | Runtime instance of an image with process isolation |
| Volume | External persistent data path outside the container layer |
| Bridge network | Default local Docker network model |
| Registry | Stores and distributes images |

## Kubernetes Quick Lookup
| Object | Responsibility |
| --- | --- |
| Pod | Smallest deployable unit |
| Deployment | Manages stateless replicated pods |
| StatefulSet | Manages identity-aware stateful pods |
| Service | Stable virtual endpoint for a pod set |
| Ingress | HTTP routing into the cluster |
| ConfigMap / Secret | Externalized config and sensitive values |

## Control Plane Quick Lookup
| Component | Responsibility |
| --- | --- |
| API server | Cluster front door and state API |
| etcd | Persistent cluster state store |
| Scheduler | Chooses nodes for unscheduled pods |
| Controller manager | Runs reconciliation loops |
| Kubelet | Node agent that manages pods |

## Reliability Quick Lookup
| Topic | Key Point |
| --- | --- |
| Liveness probe | Restarts unhealthy container |
| Readiness probe | Controls traffic eligibility |
| Rolling update | Gradual replacement of old pods |
| HPA | Scales replicas from metrics |
| PDB | Limits voluntary disruption |

## Common Failure Interpretation
| Symptom | Likely Area |
| --- | --- |
| Pod `Pending` | Scheduling, quota, node constraints, PVC binding |
| Pod `CrashLoopBackOff` | App startup failure, bad config, bad dependency assumptions |
| Service works from one pod but not outside | Service, ingress, DNS, or network policy path |
| High CPU throttling | Requests and limits mismatch |
| Data lost on restart | Used container filesystem instead of persistent volume |

## Interview One-Liners
- Containers are isolated processes, not lightweight virtual machines.
- Kubernetes is a control system built on reconciliation loops.
- A Service gives stable network identity even though pods are replaceable.
- Requests affect scheduling; limits affect runtime enforcement.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Docker-Container-Runtime-Basics.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Architecture.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Observability-and-KPIs.md]]
