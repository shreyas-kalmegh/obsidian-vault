# Docker Image Layers And Union Filesystems

## Overview
Docker images are built from stacked read-only layers plus metadata. When a container starts, Docker adds a writable layer on top, creating the illusion of a normal mutable filesystem.

## How Layers Work
- Each image build step can create a new layer.
- Layers are content-addressed and reusable across images.
- Containers from the same image share the read-only layers.
- The top writable layer captures runtime changes.

## Why This Matters
- Image pulls are more efficient when layers are reused.
- Small Dockerfile changes can invalidate later cached layers.
- Container filesystem writes are usually not the right place for durable state.

## Example
A Python image may contain:
- base OS layer
- Python runtime layer
- dependency install layer
- application code layer

If only the application code changes, earlier layers may stay cached and rebuild faster.

## Tradeoffs
- Efficient distribution and caching
- Large or badly ordered Dockerfiles create bloated images
- Excess runtime writes can hurt performance and disappear with the container

## Operational Notes
- Put stable expensive build steps earlier in the Dockerfile.
- Multi-stage builds help keep runtime images small.
- Image size affects pull time, cold start time, and registry transfer cost.

## Interview Angle
- Image layers improve reuse and distribution, not just convenience.
- The writable container layer is ephemeral by default.
- Good Dockerfiles are part performance optimization and part supply-chain hygiene.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Docker-Networking-and-Storage.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-and-Docker-Cheatsheet.md]]
