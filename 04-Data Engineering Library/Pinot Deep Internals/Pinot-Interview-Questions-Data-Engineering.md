# Pinot Interview Questions For Data Engineering

## How To Use This Note
- Aim for practical answers grounded in latency, freshness, indexing, and workload fit.
- Tie Pinot internals to analytics use cases such as dashboards, slice-and-dice queries, and near-real-time monitoring.
- Prefer clear tradeoffs over marketing language.

## Core Questions
### 1. What problem is Pinot designed to solve?
Pinot is designed for low-latency analytical queries on large event datasets, especially when freshness matters. It fits dashboards, observability, user analytics, and operational reporting better than systems optimized mainly for long-running warehouse queries.

### 2. What are the main Pinot components?
- Controller manages metadata and cluster coordination.
- Broker receives queries and routes them.
- Server stores segments and executes query operators.
- Minion handles background maintenance tasks.

### 3. What is a segment in Pinot?
A segment is the basic storage and query unit. It contains columnar data plus metadata and optional indexes. Queries are routed to servers, then evaluated segment by segment.

### 4. What is the difference between offline and realtime tables?
- Offline tables are populated by batch ingestion.
- Realtime tables ingest from streams.
- Hybrid tables expose both together so queries can combine historical and fresh data.

### 5. Why does Pinot use so many index types?
Because its target workloads vary widely. Equality filters, range predicates, text search, JSON fields, and repeated group-bys each benefit from different index structures, so Pinot lets you tailor indexes to access patterns.

### 6. What is star-tree indexing?
Star-tree is a pre-aggregation index that stores partial rollups for selected dimensions and metrics. It can make repetitive dashboard-style aggregations much faster, but increases storage and ingestion complexity.

### 7. How does Pinot achieve low query latency?
By combining segment pruning, dictionary encoding, specialized indexes, scatter-gather routing, and mostly segment-local execution. The system tries hard to avoid scanning unnecessary rows and columns.

### 8. What are upserts in Pinot?
Upserts let newer records replace older ones based on a primary key and comparison column. This is useful for mutable dimension-like data or CDC-style streams, but it adds metadata and memory overhead.

### 9. When is Pinot a poor fit?
It is a weak fit for heavy transactional updates, arbitrary multi-table relational workloads, or deep historical scans with little filtering where warehouse engines may be cheaper or simpler.

### 10. What is the difference between Pinot and Kafka?
Kafka is a durable event log for transport and replay. Pinot is a query-serving analytics store that may ingest from Kafka but is optimized for indexing and low-latency aggregations rather than message durability semantics.

## Scenario Questions
### 11. Query latency is rising after data volume doubled. What would you check?
- segment count explosion
- missing or misconfigured indexes
- skewed server assignment
- too many wide projections
- whether star-tree or partitioning assumptions no longer match the workload

### 12. Realtime data is visible later than expected. What does that suggest?
Likely issues in consuming segment ownership, stream lag, segment flush thresholds, segment commit, or broker routing to fresh realtime segments.

### 13. Why might adding servers not improve performance much?
Possible reasons:
- queries are not pruning well
- one hot table dominates traffic
- segment distribution is uneven
- broker routing or index design is the real bottleneck
- freshness tasks, not query CPU, are the limiting factor

### 14. Why can too many indexes hurt instead of help?
Each index costs build time, storage, and memory. If the index does not match common predicates, you pay ingestion and storage overhead without meaningful query benefit.

### 15. When would you choose a hybrid table?
When you need recent stream data plus larger historical data in a single logical serving layer, such as product analytics dashboards or operational KPIs with minute-level freshness.

## Strong Follow-Up Points
- Mention segment pruning when discussing speed.
- Mention hybrid tables when discussing freshness.
- Mention star-tree as a selective optimization, not a default.
- Mention upsert metadata cost when discussing mutable workloads.

## Related
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Cheatsheet.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Indexing-Strategies.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Upserts-and-Dedup.md]]
