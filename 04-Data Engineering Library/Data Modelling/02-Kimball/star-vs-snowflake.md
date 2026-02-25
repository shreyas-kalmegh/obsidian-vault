# Star vs Snowflake Schema

## Overview
Both are dimensional patterns; the main difference is dimension normalization level.

## Star Schema
Dimensions are denormalized and directly joinable to facts.

Pros:
- Fewer joins
- Simpler BI model
- Often faster user queries

Cons:
- Attribute redundancy
- More storage for repeated hierarchical data

## Snowflake Schema
Dimensions are normalized into sub-dimensions.

Pros:
- Less redundancy
- Stronger normalization/governance control

Cons:
- More joins
- Higher query complexity for analysts

## Practical Decision Framework
Prefer Star when:
- BI self-service is important
- Query latency is a priority
- Dimension sizes are manageable

Use Snowflake when:
- Dimensions are very large and hierarchical
- Governance requires strict normalization
- Teams can handle extra modeling/query complexity

## Example
Star:
- `dim_product` includes `category_name`, `brand_name`, `department_name`

Snowflake:
- `dim_product` -> `dim_category` -> `dim_department`

## Hybrid Pattern (Common in Practice)
- Keep Star in Gold for analyst usability
- Maintain normalized reference structures in upstream layers for governance

## Common Mistakes
- Snowflaking by default without proven benefit
- Over-denormalizing volatile attributes without change-control strategy

## Practical Checklist
1. Benchmark representative BI queries.
2. Evaluate analyst usability, not only storage size.
3. Decide per domain; avoid one-size-fits-all policy.

## Related Notes
- [[kimball-principles]]
- [[performance-and-cost]]
