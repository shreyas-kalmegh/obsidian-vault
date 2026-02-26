# Storage, Compute, and Cloud Services

## Storage layer in practice
Snowflake stores table data in compressed, columnar format internally. Engineers do not manage file layouts directly.

Key effect:
- Performance depends heavily on pruning and partition metadata rather than manual index tuning.

## Compute layer (virtual warehouses)
A warehouse is a cluster of compute resources used to execute SQL.

Properties:
- Size controls parallel resources and speed.
- Warehouses can be started/stopped quickly.
- Multiple warehouses can read the same data simultaneously.

Operational rule:
- Prefer right-sized warehouses per workload instead of one giant shared warehouse.

## Cloud services layer
Handles coordination services such as:
- Authentication and access checks
- Query parsing and optimization
- Metadata management
- Transaction and service orchestration

Engineering impact:
- Strong metadata and governance capabilities are native.
- Query plans depend on statistics and metadata quality.

## Caching behavior (practical)
Relevant cache types:
- Result cache: reuses query result for identical eligible query.
- Local disk cache: persisted in warehouse nodes while warehouse stays warm.

Practical tips:
- Auto-suspend too aggressively can reduce cache reuse.
- Benchmark with awareness of warm vs cold cache.

## Cost and performance connection
- Storage cost mostly tied to retained data (including historical versions).
- Compute cost tied to warehouse runtime and size.

Optimization principle:
- Reduce unnecessary compute time first (idle warehouses, inefficient queries) before over-optimizing storage.
