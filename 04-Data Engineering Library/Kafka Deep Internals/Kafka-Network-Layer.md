# Kafka Network Layer

## Overview
Kafka’s network layer is optimized for many long-lived TCP connections, large sequential transfers, and decoupling socket IO from request processing. This is a major reason Kafka scales well for streaming workloads.

## Main Components
- Acceptor thread accepts new connections.
- Network processor threads manage non-blocking socket IO using selectors.
- Requests are placed on queues for IO or request handler threads.
- Response path sends data back asynchronously.

```mermaid
flowchart LR
    A[Clients] --> B[Acceptor]
    B --> C[Network Processor Threads]
    C --> D[Request Queue]
    D --> E[Request Handler Threads]
    E --> F[Response Queue]
    F --> C
```

## Why This Design Works
- Non-blocking selectors let one thread manage many sockets.
- Request handlers focus on protocol and storage logic instead of socket waiting.
- Sequential send paths align well with batched Kafka traffic.

## Important Tuning Areas
- `num.network.threads`
- `num.io.threads`
- socket send and receive buffer sizes
- request queue size
- TLS and SASL overhead if security is enabled

## Example Bottleneck
If producers report high request latency but disks are healthy:
- network processor idle may be low
- request queue size may be growing
- increasing network threads or reducing connection churn may help

## Operational Notes
- TLS can shift Kafka from network-bound to CPU-bound.
- Very large numbers of clients can stress connection management before raw bandwidth is exhausted.
- Cross-zone latency increases request RTT and can reduce effective throughput.

## Interview Angle
- Kafka is not just a log store; its network architecture is equally important to performance.
- Non-blocking selectors explain why Kafka can manage many clients efficiently.
- Thread counts must match workload shape; more threads are not automatically better.

## Related
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Throughput-Optimizations.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Throttling.md]]
