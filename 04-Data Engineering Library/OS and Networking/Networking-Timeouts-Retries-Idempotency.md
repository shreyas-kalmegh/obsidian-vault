# Networking Timeouts, Retries, And Idempotency

## Overview
Retries are one of the easiest ways to improve apparent reliability and one of the fastest ways to create an outage. Good distributed systems pair timeout policy with bounded retries, backoff, and idempotent operations.

## Timeouts Are Resource Protection
- A timeout is not only about user experience.
- It limits how long a caller holds threads, memory, sockets, and in-flight capacity.
- Timeouts that are too long cause pileups; timeouts that are too short create unnecessary retry storms.

## Retry Rules Of Thumb
- Retry only transient failures.
- Use capped exponential backoff with jitter.
- Bound total retry budget.
- Do not let every layer retry independently.

## Why Layered Retries Explode
If a request crosses 4 services and each layer retries 3 times, the deepest dependency can see a multiplicative load spike during failures. What looks like resilience at one layer becomes overload at another.

## Idempotency
- An idempotent operation can be repeated without changing the end result after the first successful application.
- Safe retries often depend on idempotency keys, conditional writes, or deduplication logic.
- Network timeouts are ambiguous: the caller may not know whether the operation completed.

## Example
Payment request times out after the downstream successfully committed:
- client retries blindly
- duplicate charge becomes possible

With an idempotency key:
- downstream recognizes the repeated request
- same logical result is returned without duplicate side effects

## Practical Guidance
- Set separate connect timeout and request timeout when possible.
- Prefer one clear retry owner in the call path.
- Pair retries with concurrency limits and circuit breaking.
- Treat timeout metrics as capacity signals, not just transient errors.

## Interview Angle
- Timeouts protect the caller and the system.
- Retries are load multipliers.
- Idempotency is the bridge between unreliable transport and safe business operations.

## Related
- [[04-Data Engineering Library/OS and Networking/Networking-Flow-Control-Congestion-Backpressure.md]]
- [[04-Data Engineering Library/OS and Networking/Networking-DNS-Load-Balancing-Service-Discovery.md]]
