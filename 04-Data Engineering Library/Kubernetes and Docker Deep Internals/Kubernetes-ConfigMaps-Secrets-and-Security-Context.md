# Kubernetes ConfigMaps Secrets And Security Context

## Overview
Kubernetes separates configuration, sensitive values, and runtime security settings from container images. This keeps images reusable while letting operators adapt behavior per environment and enforce safer execution policies.

## ConfigMaps And Secrets
- ConfigMaps hold non-sensitive configuration
- Secrets hold sensitive values such as credentials
- Both can be exposed as environment variables or mounted files

## Security Context
- Controls user and group IDs
- Can restrict privilege escalation
- Can define filesystem and capability-related execution rules

## Example
A data pipeline image can stay the same across dev and prod while:
- endpoints come from a ConfigMap
- credentials come from a Secret
- runtime user is forced to non-root through security context

## Tradeoffs
- Better separation of config from build artifact
- More operational objects to manage
- Secret misuse is still possible if apps log values or mount them carelessly

## Operational Notes
- Secrets are not magically safe just because they use a different object type.
- Avoid baking environment-specific config into images.
- Security context defaults should be reviewed, not assumed.

## Interview Angle
- Container images should be portable; environment-specific values should live outside them.
- Security in Kubernetes is layered across image design, runtime settings, and cluster policy.
- Secrets solve distribution concerns more than they solve application misuse.

## Related
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Pod-Lifecycle.md]]
- [[04-Data Engineering Library/Kubernetes and Docker Deep Internals/Kubernetes-Observability-and-KPIs.md]]
