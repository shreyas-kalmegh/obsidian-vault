# Data Skew in Snowflake Micro-Partitions (Short Note)

## Can skew happen?
Yes. While Snowflake manages micro-partitions automatically, skew can still appear in query behavior when data distribution and access patterns are uneven.

## Common symptoms
- High scanned bytes for selective queries.
- Unstable query latency on the same table.
- Poor pruning even with filters.
- Frequent expensive scans around hot keys.

## Why it happens
- Predicates do not align with data layout.
- Heavy concentration on a few key values.
- Function-wrapped filters reduce pruning effectiveness.
- Continuous updates/inserts create overlap across partition metadata.

## Practical fixes
1. Rewrite filters for pruning-friendly predicates.
2. Add clustering keys for large, frequently filtered tables.
3. Rebuild table layout (`CTAS` with useful ordering) when fragmentation is high.
4. Use composite filter strategy (for example key + date) for hot-key workloads.
5. Consider Search Optimization for highly selective point lookups.

## Validation checklist
- Compare before/after scanned bytes and execution time.
- Inspect query profile for pruning improvement.
- Use `SYSTEM$CLUSTERING_INFORMATION` to evaluate clustering quality.

## Rule of thumb
Treat skew as a workload-and-access-pattern issue, not a manual partition-management problem.
