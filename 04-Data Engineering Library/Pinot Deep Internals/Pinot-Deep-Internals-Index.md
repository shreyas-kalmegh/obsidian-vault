# Pinot Deep Internals Index

## How To Use This Index
Read these notes in order if you want a practical mental model for how Pinot ingests, stores, indexes, routes, and serves analytical queries. The sequence starts with cluster architecture and table types, then moves into segment internals and indexing, and finally covers query execution, operations, and interview prep.

## Recommended Reading Order
### Phase 1: Core Architecture And Storage Model
1. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Architecture.md]]
2. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Offline-vs-Realtime-Tables.md]]
3. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Segment-Internals.md]]

Why first:
- These explain Pinot's controller, broker, server, and minion roles along with the table and segment abstractions that everything else builds on.

### Phase 2: Ingestion And Data Freshness
4. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Realtime-Ingestion-and-Segment-Commit.md]]
5. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Upserts-and-Dedup.md]]
6. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Minion-and-Background-Tasks.md]]

Why next:
- This layer explains how realtime data lands in Pinot, how records are updated or deduplicated, and how background maintenance keeps tables efficient.

### Phase 3: Query Path And Execution
7. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Query-Routing-and-Execution.md]]
8. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Multi-Stage-Query-Engine.md]]

Why here:
- Once storage and ingestion are clear, the broker routing model and execution engines are easier to reason about.

### Phase 4: Indexes And Performance
9. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Indexing-Strategies.md]]
10. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Star-Tree-Index.md]]
11. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Scaling-Strategies.md]]
12. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Monitoring-KPIs.md]]

Why last:
- These topics depend on understanding how Pinot stores segments and executes queries, because indexing and scaling decisions are really workload-shaping decisions.

## Fast-Track Paths
### For Data Engineering Interviews
1. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Cheatsheet.md]]
2. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Architecture.md]]
3. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Offline-vs-Realtime-Tables.md]]
4. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Indexing-Strategies.md]]
5. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Upserts-and-Dedup.md]]
6. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Interview-Questions-Data-Engineering.md]]

### For Production Debugging
1. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Monitoring-KPIs.md]]
2. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Realtime-Ingestion-and-Segment-Commit.md]]
3. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Query-Routing-and-Execution.md]]
4. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Indexing-Strategies.md]]
5. [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Scaling-Strategies.md]]

## Companion Notes
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Cheatsheet.md]] for fast recall
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Interview-Questions-Data-Engineering.md]] for DE-focused interview preparation
