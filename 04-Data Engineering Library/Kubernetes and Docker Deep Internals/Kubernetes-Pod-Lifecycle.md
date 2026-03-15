# Kubernetes Pod Lifecycle

## Overview
Pods are the basic execution unit in Kubernetes. They are created, scheduled, started, monitored, replaced, and eventually terminated as disposable units rather than permanent machines.

## Lifecycle Stages
- Pod is created and accepted by the API server.
- Scheduler assigns it to a node.
- Kubelet pulls images and starts containers.
- Readiness determines whether traffic should reach it.
- Pod may restart containers if configured.
- Pod is terminated and replaced when controllers decide it should no longer exist.

## Important States
- `Pending`: accepted but not fully scheduled or started
- `Running`: at least one container is running
- `Succeeded`: workload completed successfully
- `Failed`: workload terminated unsuccessfully
- `Unknown`: node communication state is unclear

## Why Pods Feel Ephemeral
- Controllers replace pods freely.
- Pod IPs can change.
- Local writable filesystem disappears with the pod.
- Stable identity belongs to higher-level objects, not most pods.

## Example
A Deployment rollout creates new pods with a new image.  
The old pods are terminated after the new ones pass readiness, so the service keeps working even though individual pod instances change.

## Operational Notes
- `CrashLoopBackOff` is usually an application or configuration issue, not a Kubernetes bug.
- Startup, readiness, and shutdown behavior all matter for reliable rollouts.
- Pods are a poor place to store irreplaceable local state.

## Interview Angle
- Kubernetes manages disposable compute units, not pets.
- Pod lifecycle behavior explains why configuration, probes, and Services matter so much.
- A stable application endpoint does not imply stable underlying pod instances.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Rolling-Updates-and-Probes.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-DNS-and-Service-Discovery.md]]
