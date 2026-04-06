# OS CPU Scheduling And Latency

## Overview
CPU utilization alone is a weak predictor of latency. The scheduler decides which runnable thread gets CPU time, and queueing delay on the run queue can hurt p99 latency long before the machine reaches 100 percent utilization.

## Key Ideas
- A thread can be runnable without actually running.
- Scheduler fairness is not the same as application-level usefulness.
- Oversubscription creates queueing on cores.
- CPU throttling and noisy neighbors can mimic application slowness.

## Sources Of Latency
- Too many runnable threads per core
- Frequent context switching
- Lock contention creating bursts of runnable work
- GC or runtime housekeeping stealing CPU slices
- Kernel work such as soft interrupts or packet processing

## Example
A service is limited to 2 vCPUs in a container but starts 32 worker threads:
- many requests wake up at once
- the run queue grows
- average CPU may show only moderate use over a time window
- p99 latency climbs because useful work waits its turn

This is one reason concurrency limits matter even for IO-heavy services.

## CPU-Bound Vs IO-Bound Is Not Binary
- IO-heavy systems still need CPU to serialize, encrypt, copy buffers, parse payloads, and run application logic.
- Network interrupt handling and TLS can move an "IO service" into a CPU-sensitive regime.

## Practical Guidance
- Watch run queue length, context switches, and throttling along with CPU percent.
- Size worker pools to match service behavior, not just hardware core count.
- Isolate bursty background jobs from latency-sensitive request paths where possible.

## Interview Angle
- Tail latency often comes from queueing, not from slow execution of one request.
- CPU saturation can happen at the scheduler level before dashboards show a scary average.
- Limiting concurrency is often a performance optimization, not a throughput sacrifice.

## Related
- [[04-Data Engineering Library/OS and Networking/OS-Processes-Threads-Context-Switching.md]]
- [[04-Data Engineering Library/OS and Networking/Networking-Flow-Control-Congestion-Backpressure.md]]
