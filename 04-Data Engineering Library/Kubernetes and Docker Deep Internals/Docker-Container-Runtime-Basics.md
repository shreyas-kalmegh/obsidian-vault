# Docker Container Runtime Basics

## Overview
Docker runs applications as isolated processes using kernel features such as namespaces and cgroups. Containers look machine-like from the outside, but they are really process isolation and resource control on a shared host kernel.

## Core Building Blocks
- Namespaces isolate process IDs, networking, mounts, and other kernel views.
- Cgroups control resource usage such as CPU and memory.
- Images provide the filesystem and metadata template for containers.
- The container runtime launches and supervises the actual process.

## What A Container Really Is
- A process or process group on a host
- With isolated views of system resources
- Running from an image plus a writable container layer

## Example
If two containers run the same image:
- they share the same read-only image layers
- each gets its own writable layer
- each has isolated process and network namespaces

This is why containers start much faster than virtual machines in many cases.

## Tradeoffs
- Fast startup and high density
- Shared kernel means weaker isolation than full VMs in some threat models
- Host kernel compatibility matters

## Operational Notes
- "Container crashed" often really means the main process exited.
- Resource issues usually come from cgroup limits, not from Docker magic.
- Persistent data should not rely on the container writable layer.

## Interview Angle
- Containers are isolated processes, not miniature operating systems.
- Docker adds developer and packaging ergonomics around lower-level kernel primitives.
- The host kernel is shared across containers on that node.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Docker-Image-Layers-and-Union-Filesystems.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Pod-Lifecycle.md]]
