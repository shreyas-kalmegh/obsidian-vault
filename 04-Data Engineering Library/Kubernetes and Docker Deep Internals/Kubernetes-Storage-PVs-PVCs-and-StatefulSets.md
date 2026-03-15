# Kubernetes Storage PVs PVCs And StatefulSets

## Overview
Kubernetes separates compute from persistent storage through PersistentVolumes, PersistentVolumeClaims, and storage classes. StatefulSets add stable identity and storage attachment patterns for workloads that cannot be treated as interchangeable replicas.

## Core Concepts
- PersistentVolume represents actual storage capacity.
- PersistentVolumeClaim is a workload request for storage.
- StorageClass defines provisioning behavior.
- StatefulSet manages ordered identity-aware pods with stable storage mappings.

## Why This Exists
- Pods are disposable, but state is not.
- Storage lifecycles often outlive individual containers.
- Stateful systems need identity and volume continuity across restarts.

## Example
A Kafka-like workload in Kubernetes may use a StatefulSet so broker `0` always reattaches the same volume claim after restart.  
That preserves broker identity and local log data.

## Tradeoffs
- StatefulSets provide strong identity guarantees
- Rollouts and scaling can be more operationally sensitive than Deployments
- Storage classes and dynamic provisioning simplify ops but hide infrastructure assumptions

## Operational Notes
- Many stateful failures are really storage binding or performance issues.
- Deleting a pod is not the same as deleting its persistent volume.
- Not all data systems should run in Kubernetes just because stateful primitives exist.

## Interview Angle
- StatefulSets are about identity and storage continuity, not just persistence alone.
- PVCs let applications request storage without hardcoding infrastructure details.
- Persistent storage in Kubernetes is an abstraction layer over real storage systems.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Scheduler-and-Placement.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Scaling-Strategies.md]]
