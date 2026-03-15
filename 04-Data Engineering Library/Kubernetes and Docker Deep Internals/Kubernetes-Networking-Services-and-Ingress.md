# Kubernetes Networking Services And Ingress

## Overview
Kubernetes networking gives pods routable identities inside the cluster, Services provide stable virtual endpoints, and Ingress manages external HTTP routing. These layers exist because pods are disposable and their IPs are not stable application interfaces.

## Pod Networking
- Each pod gets its own IP.
- Containers in the same pod share that network namespace.
- Pod-to-pod communication depends on the cluster network plugin.

## Services
- `ClusterIP` exposes a stable internal virtual IP
- `NodePort` exposes a port on each node
- `LoadBalancer` integrates with external load balancing where supported

Services select pods by labels and route traffic to healthy endpoints.

## Ingress
- Handles HTTP or HTTPS routing into the cluster
- Often routes by host or path
- Depends on an ingress controller to do real work

## Example
A web API Deployment may have:
- pods that come and go
- a Service called `api`
- an Ingress routing `api.company.com` to that Service

Clients use the stable endpoint, not pod IPs.

## Operational Notes
- Service problems and ingress problems are different layers.
- Readiness controls whether a pod should receive Service traffic.
- Network policies can silently block otherwise valid traffic paths.

## Interview Angle
- A Service is stable identity for unstable pods.
- Ingress is a routing abstraction, not a universal networking solution.
- Kubernetes networking is simple at the object level but subtle in production debugging.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-DNS-and-Service-Discovery.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Rolling-Updates-and-Probes.md]]
