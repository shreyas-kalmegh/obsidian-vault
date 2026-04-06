# OS And Networking Cheatsheet

## OS Core Ideas
- Process = isolation boundary
- Thread = execution unit within a process
- Context switch = scheduler plus cache penalty
- Runnable does not mean running
- Tail latency often comes from queueing, not raw compute speed

## Memory And IO
- Virtual memory gives each process isolated address space
- Major page fault usually means expensive disk access
- Page cache accelerates reads and buffers writes
- "Write completed" does not always mean "durable on disk"
- Direct IO is chosen for control and predictable behavior, often by databases

## CPU And Scheduling
- Oversubscription increases scheduler delay
- More threads can lower throughput if contention and switching rise
- CPU percent alone hides run queue pressure

## TCP And Transport
- TCP gives ordered reliable bytes, not messages
- New connections cost at least one RTT plus optional TLS setup
- Connection reuse often matters more than link bandwidth for request latency

## Pressure And Overload
- Flow control protects the receiver
- Congestion control protects the network
- Backpressure protects the system
- Retries can destroy backpressure if they are not bounded

## Discovery And Balancing
- DNS is coarse-grained routing, not real-time load balancing
- Long-lived pooled connections can keep traffic sticky to old backends
- Health checks must reflect useful readiness, not just process liveness

## Reliability
- Timeouts are resource-protection tools
- Retries need backoff, jitter, and ownership
- Idempotency turns ambiguous failures into safe retries

## Interview One-Liners
- "p99 latency is usually a queueing story before it becomes a hardware story."
- "The OS page cache is often the largest invisible performance feature in a Linux system."
- "Many network incidents are lifecycle mismatches between clients, proxies, and servers rather than packet-level failures."
