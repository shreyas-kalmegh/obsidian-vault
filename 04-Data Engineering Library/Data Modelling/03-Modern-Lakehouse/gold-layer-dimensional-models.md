# Gold Layer Dimensional Models

## Objective
Convert Silver entities/events into query-optimized fact and dimension models for BI and analytics.

## Typical Output
- `dim_customer`, `dim_product`, `dim_date`
- `fct_orders`, `fct_returns`, `fct_revenue_daily`

## Checklist
- [ ] Grain declaration per fact
- [ ] SCD strategy per mutable attribute
- [ ] Conformed dimensions reused across marts
- [ ] Data tests for PK/FK, nulls, duplicates

## Common Mistakes
- Building Gold as one wide denormalized table
- No semantic ownership for metrics

## Interview Prompts
- Show how you design a gold model for subscription analytics.

## Related Notes
- [[medallion-architecture]]
- [[kimball-principles]]
