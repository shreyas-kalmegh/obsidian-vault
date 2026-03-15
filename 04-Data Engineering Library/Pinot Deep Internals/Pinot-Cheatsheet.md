# Pinot Deep Internals Cheatsheet

## Core Mental Model
- Pinot is a distributed OLAP store optimized for low-latency aggregations and filtering on immutable segments.
- Brokers route queries, servers scan and aggregate segments, controllers manage metadata, and minions run background tasks.
- Data is organized into offline and realtime tables, each made of many segments.
- Query speed comes from segment pruning, dictionary encoding, and the right index mix more than from raw hardware alone.

## Cluster Roles Quick Lookup
| Component | Responsibility |
| --- | --- |
| Controller | Table metadata, segment assignment, ingestion orchestration |
| Broker | Query routing, fan-out, merge, reduce |
| Server | Hosts segments and executes scan/filter/aggregate work |
| Minion | Background tasks such as merge, rollup, purge, conversion |

## Table Model Quick Lookup
| Table Type | Typical Use |
| --- | --- |
| Offline | Batch-loaded historical data |
| Realtime | Fresh streaming ingestion from Kafka or similar sources |
| Hybrid | Same logical dataset exposed through offline + realtime tables |

## Index Quick Lookup
| Index | Best For |
| --- | --- |
| Dictionary | Encoded column storage and fast predicate evaluation |
| Inverted | Equality and `IN` filters on selective columns |
| Range | Numeric and range-heavy filters |
| Bloom | Fast negative checks on high-cardinality lookup columns |
| JSON / Text / FST | Semi-structured and text search patterns |
| Star-tree | Pre-aggregated rollups for repeated group-by workloads |

## Realtime Ingestion Quick Lookup
| Concept | Key Point |
| --- | --- |
| Consuming segment | Mutable in-memory segment receiving stream data |
| Segment flush | Triggered by row count, time, or size thresholds |
| Segment commit | Publishes a completed segment to the cluster |
| LLC | Partition-level consumption with deterministic ownership |

## Query Quick Lookup
| Topic | Key Point |
| --- | --- |
| Broker routing | Tries to hit only relevant servers and segments |
| Segment pruning | Skips unnecessary work using metadata and indexes |
| Single-stage engine | Traditional scatter-gather execution |
| Multi-stage engine | Better support for joins and distributed stages |

## Common Failure Interpretation
| Symptom | Likely Area |
| --- | --- |
| High query p95, low CPU | Poor pruning or missing indexes |
| Realtime freshness lag | Stream ingestion, flush, or commit issues |
| One server much hotter than others | Bad segment distribution or skewed routing |
| High heap pressure | Large dictionaries, wide projections, or oversized consuming segments |
| Slow hybrid queries | Offline/realtime overlap or poor time boundary behavior |

## Interview One-Liners
- Pinot is built for user-facing analytics where latency matters more than full warehouse-style flexibility.
- Segments are Pinot's core storage and execution unit.
- Indexes in Pinot are workload-specific accelerators, not features to turn on blindly.
- Hybrid tables are a freshness pattern, not a separate storage engine.

## Related
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Architecture.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Indexing-Strategies.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Query-Routing-and-Execution.md]]
