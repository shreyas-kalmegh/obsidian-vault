# OS And Networking Interview Questions

## Operating Systems
### Why can a service have high latency even when CPU utilization is not near 100 percent?
- Because requests may be waiting on the run queue, contending on locks, stalling on page faults, or getting delayed by context-switch overhead. CPU average hides scheduler queueing and memory stalls.

### What is the difference between a process and a thread, and why does it matter in backend systems?
- A process provides memory isolation and failure isolation. Threads share address space and file descriptors, which makes communication cheaper but raises synchronization risk. This matters for concurrency design, crash blast radius, and memory usage.

### What is a page fault, and when is it a real problem?
- A page fault happens when the CPU cannot translate or access a page with the current mapping state. Minor faults are often cheap; major faults require disk IO and can create large latency spikes.

### Why is page cache so important?
- It turns repeated file access into memory-speed access, smooths writes, and reduces device IO. But it also means application performance depends on memory pressure and writeback behavior, not just disk hardware.

### When would you choose direct IO?
- When the application already has its own cache or buffer manager, wants predictable latency, and wants to avoid double caching or page cache pollution.

## Networking
### Why is TCP called a byte-stream protocol, and why does that matter?
- Because it preserves order and reliability of bytes, not message boundaries. Applications must define framing themselves, otherwise reads and writes will not line up cleanly.

### What is the practical cost of creating too many short-lived connections?
- More handshake latency, more CPU for TCP and TLS setup, more socket churn, more pressure on ephemeral ports and accept queues, and often worse tail latency.

### Explain flow control vs congestion control.
- Flow control protects the receiver from being overwhelmed. Congestion control protects the network path from overload. They are related but solve different problems.

### Why do retries make outages worse?
- Because they multiply load exactly when the dependency is already struggling. Without backoff, jitter, retry budgets, and idempotency, retries turn slowness into collapse.

### Why does DNS-based service discovery sometimes lead to uneven traffic?
- Because clients cache answers and often reuse long-lived connections. Even if DNS rotates records, existing connections may stay pinned to the same backends.

## Senior / Staff Follow-Ups
### How would you debug rising p99 latency in a service that looks healthy on CPU and memory dashboards?
- Check run queue pressure, context switches, throttling, GC, page faults, disk writeback, connection pool saturation, timeout rates, and downstream queue growth. The goal is to locate where queueing begins.

### A downstream dependency is timing out. How do you stop the failure from cascading?
- Reduce concurrency, cap retries, add backoff and jitter, tighten ownership of retry policy, shed low-priority work, and verify idempotency before retrying writes.

### What is one common mistake teams make when scaling services?
- They add replicas without examining connection reuse, DNS caching, and load balancer behavior, so traffic remains uneven and the new capacity is underused.

## Related
- [[04-Data Engineering Library/OS and Networking/OS-Networking-Cheatsheet.md]]
- [[04-Data Engineering Library/OS and Networking/OS-Networking-Index.md]]
