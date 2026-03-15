# Pinot Scaling Strategies

## Overview
Scaling Pinot is about balancing segment count, query fan-out, index efficiency, table design, and node specialization. More servers help only when routing, assignment, and workload shape actually let the cluster use them well.

## Common Scaling Levers
- Add servers to spread segment storage and scan load.
- Add brokers to handle higher query concurrency.
- Tune segment size so per-segment overhead stays reasonable.
- Split very hot workloads into separate tables or tenants.
- Use the right indexes so scale comes from less work, not just more hardware.

## Data Scaling
- More data often means more segments, not just more bytes.
- Segment explosion increases routing cost, open metadata, and tail latency.
- Compaction or merge-rollup tasks can be just as important as adding nodes.

## Query Scaling
- High concurrency stresses brokers and the slowest servers first.
- Wide scans can make every query expensive even on large clusters.
- Repeated dashboard workloads often scale better with star-tree or better pruning than with brute-force hardware.

## Realtime Scaling
- Stream partitioning should align with server capacity and ownership patterns.
- Tiny consuming segments create a large control-plane burden.
- Freshness and efficiency usually need different flush thresholds than raw throughput does.

## Example
A cluster adds 10 servers, but p95 query latency barely improves.

Possible reasons:
- queries still fan out to nearly all segments
- hot tables dominate traffic
- missing indexes force large scans
- segment distribution remains skewed

## Interview Angle
- Pinot scale limits are frequently indexing and segment-design limits before pure CPU limits.
- Adding brokers helps concurrency; adding servers helps storage and scan load.
- Good pruning is a scaling strategy, not just a query optimization detail.

## Related
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Star-Tree-Index.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Monitoring-KPIs.md]]
