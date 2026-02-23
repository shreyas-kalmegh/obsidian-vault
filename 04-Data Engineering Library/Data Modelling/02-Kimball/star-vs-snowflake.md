# Star vs Snowflake Schema

## Star Schema
- Denormalized dimensions.
- Fewer joins, faster BI queries, easier to understand.

## Snowflake Schema
- Normalized dimensions.
- Less redundancy but more joins and complexity.

## Decision Guide
- Prefer star for analytics and dashboard performance.
- Use snowflake when strong normalization/governance needs dominate.

## Checklist
- [ ] Query pattern and SLA evaluated
- [ ] Storage vs performance tradeoff documented

## Common Mistakes
- Snowflaking dimensions unnecessarily
- Over-denormalizing without quality controls

## Interview Prompts
- When would you choose snowflake over star in modern warehouses?

## Related Notes
- [[kimball-principles]]
- [[performance-and-cost]]
