# Kubernetes Rolling Updates And Probes

## Overview
Kubernetes uses rolling updates to replace pods gradually and probes to decide when containers are healthy enough to restart or receive traffic. Together, they form a big part of production reliability.

## Probe Types
- Liveness probe decides whether a container should be restarted.
- Readiness probe decides whether a pod should receive traffic.
- Startup probe protects slow-starting apps from premature restarts.

## Rolling Update Behavior
- New pods are created gradually.
- Old pods are removed as new ones become ready.
- Update parameters control how many can be unavailable or added temporarily.

## Example
If readiness is too optimistic:
- new pods start receiving traffic too early
- requests fail during warmup
- rollout appears healthy from Kubernetes' perspective but users see errors

## Tradeoffs
- Safer changes with controlled blast radius
- More moving parts in app startup and shutdown behavior
- Bad probes can create restart loops or false health

## Operational Notes
- Readiness mistakes often hurt availability more than liveness mistakes.
- Graceful shutdown matters because terminated pods may still be handling traffic.
- Rollout debugging should include app logs and probe events together.

## Interview Angle
- Liveness is about restart, readiness is about traffic.
- A successful rollout requires both correct probe logic and sane update strategy.
- Kubernetes can automate deployment safely only if the application exposes meaningful health signals.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Pod-Lifecycle.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Observability-and-KPIs.md]]
