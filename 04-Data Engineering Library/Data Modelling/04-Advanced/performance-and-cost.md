# Performance and Cost in Data Models

## Levers
- Partitioning and clustering keys
- File size and compaction strategy
- Join cardinality and dimension design
- Pre-aggregation where justified

## Checklist
- [ ] Hot queries profiled
- [ ] Partition pruning validated
- [ ] Expensive joins reviewed
- [ ] Storage and compute costs tracked

## Common Mistakes
- Over-partitioning small datasets
- Ignoring skew in distributed joins

## Interview Prompts
- How do you tune a slow star-schema dashboard query?

## Related Notes
- [[star-vs-snowflake]]
- [[indexes]]
