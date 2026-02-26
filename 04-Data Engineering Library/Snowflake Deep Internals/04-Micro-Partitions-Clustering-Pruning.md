# Micro-Partitions, Clustering, and Pruning

## Micro-partitions
Snowflake stores table data in immutable micro-partitions with metadata (min/max values, etc.).

Why this is important:
- Query pruning can skip irrelevant partitions, reducing scan cost and runtime.
- Good filtering patterns directly improve performance.

## Partition pruning in real workloads
Pruning works best when query predicates align with data distribution.

Example good filter pattern:
- `WHERE event_date >= CURRENT_DATE - 7`

Common anti-pattern:
- Wrapping filter columns in functions (`DATE(event_ts) = ...`) can weaken pruning.

## Clustering keys
Snowflake can maintain clustering depth for large tables where natural ordering is poor.

Use clustering when:
- Tables are large and frequently filtered by specific columns.
- Query latency is unstable due to poor pruning.

Do not use blindly:
- Clustering has maintenance cost.
- Small or infrequently queried tables usually do not need it.

## Search optimization (high-level)
For selective point-lookups on huge tables, search optimization service can help.

Guidance:
- Reserve for truly selective access patterns after baseline tuning.

## Practical tuning workflow
1. Identify high-cost queries from query history.
2. Check scanned bytes vs returned rows.
3. Improve predicates and model grain.
4. Evaluate clustering/search optimization only when required.

## Data modeling tie-in
Partition behavior is influenced by load patterns and data layout:
- Append-heavy fact tables naturally benefit from temporal pruning.
- Frequent wide updates can fragment version history and increase scan overhead.
