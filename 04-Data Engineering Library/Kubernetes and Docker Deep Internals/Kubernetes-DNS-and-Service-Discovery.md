# Kubernetes DNS And Service Discovery

## Overview
Kubernetes service discovery is usually built on DNS names backed by Services rather than on direct pod addressing. This lets applications target stable logical endpoints while the actual pod set changes underneath.

## Core Model
- Services get DNS names inside the cluster.
- Pods can resolve those names through cluster DNS.
- The resolved destination maps to current healthy endpoints selected by the Service.

## Why This Matters
- Pod IPs are ephemeral.
- Scaling events change endpoint sets continuously.
- Applications need a stable lookup pattern that survives restarts and rollouts.

## Example
A streaming app may connect to `redis.default.svc.cluster.local` instead of a specific pod IP.  
If Redis pods are replaced behind the Service, the client target name stays the same.

## Common Pitfalls
- Hardcoding pod IPs
- assuming local Docker hostname behavior matches Kubernetes
- confusing DNS resolution success with actual endpoint readiness

## Operational Notes
- DNS working does not guarantee the app behind the Service is ready.
- Endpoint selection still depends on labels and readiness.
- Namespace scoping matters for short service names.

## Interview Angle
- Kubernetes service discovery is really Service discovery, not pod discovery.
- DNS is only one step in the request path.
- Stable names plus replaceable pods are a core Kubernetes design pattern.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Networking-Services-and-Ingress.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Pod-Lifecycle.md]]
