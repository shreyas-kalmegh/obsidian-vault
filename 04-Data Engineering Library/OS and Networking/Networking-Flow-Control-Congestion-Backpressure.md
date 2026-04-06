# Networking Flow Control, Congestion Control, And Backpressure

## Overview
Not all slowness on a network means packet loss. Modern distributed systems slow down for several different reasons, and it is important to separate receiver-side limits, network-wide congestion, and application-level overload.

## Flow Control
- Protects the receiver from being overwhelmed.
- TCP uses the receive window to tell the sender how much more data can be accepted.
- If the receiver application reads slowly, the receive buffer fills and the sender must slow down.

## Congestion Control
- Protects the network path from overload.
- TCP infers congestion from loss, delay, or explicit signals depending on the algorithm.
- The sender adjusts its congestion window to avoid collapsing throughput for everyone on the path.

## Application Backpressure
- Happens above TCP when a service or queue cannot process input as fast as it arrives.
- Common symptoms are growing request queues, high response time, and retries making things worse.
- TCP may still be healthy while the application is overloaded.

## Practical Mental Model
- Flow control says "the receiver is full."
- Congestion control says "the network path looks overloaded."
- Backpressure says "the system as a whole must slow producers down."

## Example
A consumer service stops reading from a socket quickly enough:
- socket receive buffer fills
- TCP advertised window shrinks
- sender throughput drops
- upstream request queue grows

If the upstream now retries aggressively, the real problem becomes application-level overload, not just TCP flow control.

## Why This Matters In Data Systems
- Streaming pipelines often fail from pressure propagation, not hard crashes.
- A slow sink can create lag in consumers, which increases queue depth, memory use, and retry load upstream.
- Senior engineers should reason about where the pressure starts and where it gets amplified.

## Interview Angle
- Flow control and congestion control solve different problems.
- Retries can defeat backpressure if not bounded.
- Stable systems slow down intentionally before they fall over.

## Related
- [[04-Data Engineering Library/OS and Networking/Networking-Timeouts-Retries-Idempotency.md]]
- [[04-Data Engineering Library/OS and Networking/OS-CPU-Scheduling-Latency.md]]
