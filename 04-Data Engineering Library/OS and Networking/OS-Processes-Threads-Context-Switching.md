# OS Processes, Threads, And Context Switching

## Overview
Processes provide isolation boundaries. Threads provide concurrency within that boundary. Context switching is the hidden tax paid when the CPU stops running one execution stream and starts running another.

## Process Vs Thread
- A process has its own virtual address space, file descriptor table, credentials, and failure boundary.
- Threads in the same process share heap, code, and open file descriptors.
- Each thread still has its own stack, registers, and scheduling state.

## Why Threads Feel Cheap But Are Not Free
- Creating a thread is usually cheaper than creating a process.
- Synchronization, cache invalidation, lock contention, and scheduler overhead can dominate performance before raw CPU is fully utilized.
- Too many runnable threads often hurts latency more than it helps throughput.

## What Happens During A Context Switch
- The kernel saves the current thread's CPU register state.
- The scheduler selects the next runnable thread.
- The CPU loads the next thread's register state.
- Caches and TLB state may become less useful, which increases memory access cost after the switch.

```mermaid
flowchart LR
    A[Thread A Running] --> B[Timer Interrupt or Block]
    B --> C[Kernel Scheduler]
    C --> D[Save A State]
    D --> E[Load B State]
    E --> F[Thread B Running]
```

## User Threads Spend Time In Four Buckets
- Running on CPU
- Runnable but waiting for CPU
- Blocked on IO or locks
- Sleeping on timers

A system can look CPU-light overall while still having high latency because threads are spending too much time runnable but not scheduled.

## Practical Example
An API service has 400 request threads on an 8-core machine:
- throughput may initially rise because more requests are in flight
- tail latency then increases because the scheduler constantly rotates runnable threads
- lock contention increases
- cache locality gets worse

In practice, bounded worker pools usually outperform unbounded thread growth.

## Interview Angle
- Processes are isolation units; threads are scheduling units.
- High thread count is not the same as high parallelism.
- Context switching hurts not just CPU time but also cache efficiency and tail latency.

## Related
- [[04-Data Engineering Library/OS and Networking/OS-CPU-Scheduling-Latency.md]]
- [[04-Data Engineering Library/OS and Networking/OS-Virtual-Memory-Paging-Page-Cache.md]]
