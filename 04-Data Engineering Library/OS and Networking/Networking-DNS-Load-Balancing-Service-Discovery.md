# Networking DNS, Load Balancing, And Service Discovery

## Overview
Service-to-service communication starts before the first packet reaches the target application. Name resolution, load balancer choice, health state, and connection reuse all shape where traffic actually goes.

## DNS Basics That Matter Operationally
- DNS maps names to IP addresses, not to application instances directly.
- Results are cached by clients, runtimes, operating systems, and intermediate resolvers.
- TTL controls how long answers may be cached, but some clients cache more aggressively than expected.

## Why DNS Alone Is Not Enough
- DNS does not understand application load.
- Low TTLs increase query volume and still do not guarantee instant traffic shifts.
- DNS is good for coarse routing, not per-request balancing.

## Load Balancing Layers
- L4 load balancers distribute based on connection metadata such as IP and port.
- L7 load balancers can route using HTTP path, headers, hostnames, or application awareness.
- Internal service meshes and sidecars often add another balancing layer inside the cluster.

## Service Discovery Patterns
- Client-side discovery: client resolves endpoints and chooses the target.
- Server-side discovery: client talks to a stable VIP or proxy which chooses the target.

## Practical Example
A service scales from 10 to 50 pods:
- DNS may return a changing set of IPs
- clients with long-lived pooled connections may keep using only the old subset
- traffic can remain uneven even though DNS records look correct

This is why balancing behavior must be reasoned about together with connection reuse.

## Failure Modes
- Stale DNS cache keeps traffic flowing to drained hosts.
- Health checks pass but the application is overloaded at the tail.
- Cross-zone or cross-region routing appears during failover and increases latency.

## Interview Angle
- DNS answers the "where can I try?" question, not "which backend is best right now?"
- Load balancing quality depends on connection lifecycle, cache behavior, and health signal quality.
- Discovery and balancing are coupled design decisions, not independent boxes on a diagram.

## Related
- [[04-Data Engineering Library/OS and Networking/Networking-Connection-Pooling-Keepalive.md]]
- [[04-Data Engineering Library/OS and Networking/Networking-Timeouts-Retries-Idempotency.md]]
