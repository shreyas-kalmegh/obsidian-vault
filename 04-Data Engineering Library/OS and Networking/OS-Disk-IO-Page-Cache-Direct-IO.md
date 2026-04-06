# OS Disk IO, Page Cache, And Direct IO

## Overview
Most application reads and writes do not go directly from user space to disk. They usually go through the kernel page cache first. That cache smooths IO, batches writes, and reduces physical disk access, but it can also create confusing performance behavior.

## Buffered IO
- Reads are often satisfied from page cache if data is already resident.
- Writes typically go to page cache first and are flushed to disk later.
- This makes writes look fast initially even though durable persistence may happen later.

## Why Page Cache Helps
- Sequential reads become much cheaper after warmup.
- Repeated access to hot files avoids repeated device IO.
- Writeback lets the kernel coalesce small writes into larger operations.

## Why Page Cache Can Mislead
- Benchmark results may mostly measure memory speed rather than storage speed.
- An application can report "write completed" before data is physically durable.
- Dirty page buildup can later cause bursty writeback and latency spikes.

## Direct IO
- Direct IO bypasses the page cache for application data paths.
- It reduces cache pollution for large streaming workloads.
- It is often used by databases that want explicit control of caching and flush behavior.

## Tradeoffs
- Buffered IO is simpler and often faster for general-purpose applications.
- Direct IO can be better for predictable latency and large scans.
- Bypassing page cache means the application must manage more of its own read-ahead and buffering strategy.

## Example
Kafka log segments benefit heavily from sequential append and the OS page cache:
- recent writes are likely still in cache
- consumers may read hot data without touching disk
- once data ages out, fetch latency depends more on device performance

A database using direct IO avoids double caching because it already maintains its own buffer pool.

## Practical Debugging Clues
- High disk utilization with low application throughput can indicate random IO or writeback pressure.
- Good average latency with bad tail latency can come from flush bursts.
- Memory pressure can slow IO even if the disk itself is healthy because cache hit rate falls.

## Interview Angle
- "Write returned" and "data is durable" are not always the same event.
- Page cache is an optimization layer, not durable storage by itself.
- Direct IO is usually chosen for control and predictability, not because page cache is bad.

## Related
- [[04-Data Engineering Library/OS and Networking/OS-Virtual-Memory-Paging-Page-Cache.md]]
- [[04-Data Engineering Library/OS and Networking/Networking-Connection-Pooling-Keepalive.md]]
