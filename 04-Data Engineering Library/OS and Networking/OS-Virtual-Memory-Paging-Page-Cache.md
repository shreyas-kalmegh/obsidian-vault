# OS Virtual Memory, Paging, And Page Cache

## Overview
Virtual memory gives each process the illusion of a large private address space. The operating system maps that virtual space to physical memory pages and uses disk as an overflow layer when memory pressure rises.

## Core Concepts
- Virtual addresses are translated to physical addresses through page tables.
- Memory is managed in pages, not arbitrary byte ranges.
- A page fault happens when the required page mapping is missing or not resident in RAM.
- Minor faults usually resolve from existing kernel-managed state.
- Major faults require disk IO and can be very expensive.

## Why Virtual Memory Matters In Real Systems
- It isolates processes from one another.
- It lets the kernel lazily load executable pages and file-backed mappings.
- It allows the page cache to make file IO look memory-like after warmup.

## Anonymous Memory Vs File-Backed Memory
- Anonymous memory backs heap and stack pages.
- File-backed memory comes from mapped files and the page cache.
- Under pressure, file-backed pages are often easier to reclaim than dirty anonymous pages.

## Paging Under Pressure
- If RAM gets tight, the kernel reclaims clean cache pages first.
- Dirty pages may need writeback before they can be reclaimed.
- If that is still insufficient, the system may start swapping anonymous memory.
- Heavy swap activity usually destroys latency-sensitive workloads.

## Example
A Spark executor or JVM service allocates too much heap:
- the process fits at startup
- page cache shrinks
- read performance degrades because files must be fetched again from disk
- eventually the host starts swapping or the process is killed by OOM policy

This is why "free memory is wasted memory" is only half the story. You want memory used productively, not consumed in a way that destroys cache effectiveness.

## Practical Mental Model
- RAM is shared between application memory and kernel cache.
- A memory-heavy process can indirectly slow down disk-heavy neighbors.
- Latency spikes can come from page faults and reclaim work, not only CPU saturation.

## Interview Angle
- Virtual memory is about isolation, indirection, and efficiency, not just "more memory."
- Major page faults are latency events.
- Page cache is often one of the biggest hidden performance accelerators in Linux systems.

## Related
- [[04-Data Engineering Library/OS and Networking/OS-Disk-IO-Page-Cache-Direct-IO.md]]
- [[04-Data Engineering Library/OS and Networking/OS-CPU-Scheduling-Latency.md]]
