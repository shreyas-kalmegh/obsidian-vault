# Kubernetes Controllers And Reconciliation

## Overview
Kubernetes controllers continuously compare desired state to actual state and take action to close the gap. This reconciliation model is the heart of Kubernetes rather than a background detail.

## How Reconciliation Works
1. Desired state is stored in the API.
2. Controllers watch relevant objects.
3. If actual state differs, controllers create, update, or delete resources.
4. The loop repeats continuously.

## Common Controllers
- Deployment controller manages ReplicaSets
- ReplicaSet controller maintains the right number of pods
- Job controller tracks completion-oriented workloads
- StatefulSet controller manages ordered, identity-aware pods

## Example
If a Deployment wants 5 replicas but only 4 pods are running, the ReplicaSet controller creates another pod. If 6 are running, one is terminated.

This is why manual pod deletion usually does not "fix" anything for long unless desired state is changed too.

## Why It Matters
- Recovery is automated
- Drift is corrected continuously
- Humans and controllers can both write cluster state through the API

## Operational Notes
- If the wrong thing keeps coming back, check the controller object, not just the pod.
- Reconciliation can amplify bad config quickly because the cluster faithfully tries to enforce it.
- Debugging often means understanding which controller owns a resource.

## Interview Angle
- Kubernetes is a feedback-control system.
- Controllers do not execute once; they run as ongoing loops.
- Desired state is authoritative unless a controller itself is unhealthy.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Architecture.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Rolling-Updates-and-Probes.md]]
