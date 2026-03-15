# Kubernetes Autoscaling And Capacity

## Overview
Kubernetes scaling is about replicas, resource requests, and node capacity working together. Autoscaling helps only when the chosen metric matches the true bottleneck and the cluster can actually place the extra work.

## Main Scaling Layers
- Horizontal Pod Autoscaler changes replica count
- Vertical scaling changes pod resource sizing
- Cluster autoscaling changes node capacity where supported

## Why Autoscaling Can Mislead
- CPU may not reflect queue depth or latency bottlenecks
- Wrong requests distort scheduler behavior
- Slow startup times reduce scaling usefulness for bursty loads

## Example
A streaming API scales from 4 to 12 replicas on CPU.  
Latency still stays high because the downstream database is saturated and each new pod opens more connections.

The metric triggered scaling, but the bottleneck was elsewhere.

## Operational Notes
- Requests should reflect realistic steady-state needs.
- Overcommitted clusters can look efficient until failure or noisy neighbors appear.
- Capacity planning is still needed even with autoscaling.

## Interview Angle
- Autoscaling is not automatic performance engineering.
- HPA adds replicas; it does not fix bad code or slow dependencies.
- Scheduler fit and node availability matter as much as autoscaling policies.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Scheduler-and-Placement.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Scaling-Strategies.md]]
