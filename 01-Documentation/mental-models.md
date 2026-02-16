# Mental Models for Data Platform Engineering

## Systems Thinking
- Every component is part of a larger system.
- Look for bottlenecks, saturation, and flow control.

## Performance First
- CPU cache and data locality matter more than code elegance.
- Network is slow, disk is slower.

## Distributed Mindset
- Everything can fail at any time.
- Design for retries, idempotency, and backpressure.

## Data Guarantees
- Understand ordering, consistency, durability, atomicity.
- Prefer deterministic behavior in pipelines.

## Rust Mindset
- Ownership prevents entire classes of bugs.
- Favor immutability and explicit state transitions.
