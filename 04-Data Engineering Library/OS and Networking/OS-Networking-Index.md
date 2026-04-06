# OS And Networking Index

## How To Use This Index
Read these notes in order if you want a practical mental model for how requests move through a distributed system and how the operating system shapes latency, throughput, and failure behavior. The sequence starts with local compute and memory mechanics, then moves into storage and network transport, and finally covers production resilience patterns.

## Recommended Reading Order
### Phase 1: OS Foundations
1. [[04-Data Engineering Library/OS and Networking/OS-Processes-Threads-Context-Switching.md]]
2. [[04-Data Engineering Library/OS and Networking/OS-Virtual-Memory-Paging-Page-Cache.md]]
3. [[04-Data Engineering Library/OS and Networking/OS-Disk-IO-Page-Cache-Direct-IO.md]]
4. [[04-Data Engineering Library/OS and Networking/OS-CPU-Scheduling-Latency.md]]

Why first:
- These explain what a process really owns, how threads share state, why context switches are expensive, and how memory and disk behavior affect application latency.

### Phase 2: Network Transport And Request Path
5. [[04-Data Engineering Library/OS and Networking/Networking-TCP-Connection-Lifecycle.md]]
6. [[04-Data Engineering Library/OS and Networking/Networking-Flow-Control-Congestion-Backpressure.md]]
7. [[04-Data Engineering Library/OS and Networking/Networking-DNS-Load-Balancing-Service-Discovery.md]]
8. [[04-Data Engineering Library/OS and Networking/Networking-Connection-Pooling-Keepalive.md]]

Why next:
- These notes explain how clients establish connections, how traffic slows down under pressure, how services find each other, and why connection reuse often matters more than people expect.

### Phase 3: Reliability And Production Behavior
9. [[04-Data Engineering Library/OS and Networking/Networking-Timeouts-Retries-Idempotency.md]]
10. [[04-Data Engineering Library/OS and Networking/OS-Networking-Interview-Questions.md]]

Why last:
- These connect internals to system design and incident response, which is where senior and staff interview discussions usually go.

## Fast-Track Paths
### For Senior And Staff Interviews
1. [[04-Data Engineering Library/OS and Networking/OS-Networking-Cheatsheet.md]]
2. [[04-Data Engineering Library/OS and Networking/OS-Processes-Threads-Context-Switching.md]]
3. [[04-Data Engineering Library/OS and Networking/OS-Virtual-Memory-Paging-Page-Cache.md]]
4. [[04-Data Engineering Library/OS and Networking/Networking-TCP-Connection-Lifecycle.md]]
5. [[04-Data Engineering Library/OS and Networking/Networking-Flow-Control-Congestion-Backpressure.md]]
6. [[04-Data Engineering Library/OS and Networking/Networking-Timeouts-Retries-Idempotency.md]]
7. [[04-Data Engineering Library/OS and Networking/OS-Networking-Interview-Questions.md]]

### For Production Debugging
1. [[04-Data Engineering Library/OS and Networking/OS-Disk-IO-Page-Cache-Direct-IO.md]]
2. [[04-Data Engineering Library/OS and Networking/OS-CPU-Scheduling-Latency.md]]
3. [[04-Data Engineering Library/OS and Networking/Networking-Flow-Control-Congestion-Backpressure.md]]
4. [[04-Data Engineering Library/OS and Networking/Networking-Connection-Pooling-Keepalive.md]]
5. [[04-Data Engineering Library/OS and Networking/Networking-DNS-Load-Balancing-Service-Discovery.md]]
6. [[04-Data Engineering Library/OS and Networking/Networking-Timeouts-Retries-Idempotency.md]]
7. [[04-Data Engineering Library/OS and Networking/Bash-Shell-Debugging-Cheatsheet.md]]
8. [[04-Data Engineering Library/OS and Networking/Data-Engineering-Debugging-Cheatsheet.md]]

## Companion Notes
- [[04-Data Engineering Library/OS and Networking/OS-Networking-Cheatsheet.md]] for quick recall
- [[04-Data Engineering Library/OS and Networking/OS-Networking-Interview-Questions.md]] for interview preparation
- [[04-Data Engineering Library/OS and Networking/Bash-Shell-Debugging-Cheatsheet.md]] for common production debugging commands
- [[04-Data Engineering Library/OS and Networking/Data-Engineering-Debugging-Cheatsheet.md]] for Kafka, Spark, and JVM-centric debugging
