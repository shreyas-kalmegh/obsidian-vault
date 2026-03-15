# Docker Networking And Storage

## Overview
Docker gives containers their own network namespaces and connectable virtual networks, while storage is handled through bind mounts and volumes. Both matter because containers are ephemeral by design but real applications still need connectivity and persistence.

## Networking Basics
- Containers can be attached to bridge, host, or overlay-style networks depending on environment.
- Port publishing maps host ports to container ports.
- Inside a Docker network, containers can often reach each other by name.

## Storage Basics
- Bind mounts map a host path into a container.
- Volumes are Docker-managed persistent storage abstractions.
- The container writable layer is not a safe persistence strategy.

## Example
A local Postgres container can store database files in a named volume.  
If the container is deleted and recreated with the same volume, the data survives.

Without that volume, data in the writable layer disappears with the container.

## Tradeoffs
- Easy local development workflow
- Host path mounts can create environment-specific behavior
- Port mapping and local DNS assumptions do not translate directly to Kubernetes

## Operational Notes
- "Works in Docker" often hides host-mounted config or filesystem assumptions.
- Local bridge networking is simpler than cluster networking.
- Volume and mount choices affect portability and recovery behavior.

## Interview Angle
- Docker persistence is external to the container lifecycle.
- Networking in local Docker setups is much simpler than Kubernetes networking.
- Many production migration issues come from confusing local container convenience with distributed cluster reality.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Networking-Services-and-Ingress.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Storage-PVs-PVCs-and-StatefulSets.md]]
