# Query Performance Tuning

## Start with evidence
Use query history and profile before changing SQL blindly.

Key metrics to inspect:
- Total execution time
- Queue time vs execution time
- Bytes scanned
- Spill to local/remote storage

## Common bottlenecks
- Poor pruning causing massive scans
- Large joins with skewed keys
- Repeated expensive CTE logic
- Window functions over very large unfiltered sets

## SQL-level tuning patterns
- Filter early where possible.
- Select only required columns.
- Pre-aggregate before wide joins when it reduces row volume.
- Replace repeated heavy subqueries with intermediate tables for reuse.

## Join tuning practicals
- Ensure join keys are compatible types.
- Watch for accidental many-to-many joins.
- Use surrogate keys consistently in marts.

## Materialized views and dynamic tables
These can offload repeated compute for common patterns.

Use when:
- Same expensive transformation is reused frequently.
- Freshness requirements are clear and manageable.

Tradeoff:
- Additional maintenance and compute cost.

## Warehouse vs SQL tuning
Decision rule:
- If queue time dominates, adjust concurrency/warehouse.
- If execution time dominates with high scan volume, optimize SQL/modeling first.
