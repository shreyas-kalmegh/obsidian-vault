# Gold Layer Dimensional Models

## Overview
Gold models translate canonical Silver data into business-consumable facts, dimensions, and curated marts.
Gold should optimize for metric trust, query performance, and semantic clarity.

## Typical Gold Outputs
- Dimensions: `dim_customer`, `dim_product`, `dim_date`
- Facts: `fct_order_line`, `fct_return_line`, `fct_subscription_daily`
- KPI marts: `mart_revenue_daily`, `mart_retention_monthly`

## Design Approach
1. Start from business questions and KPI definitions.
2. Declare fact grain explicitly.
3. Reuse conformed dimensions.
4. Apply SCD strategy where history is required.
5. Publish metric contracts in semantic layer.

## Example: Subscription Analytics Gold
- `fct_subscription_event` (transaction fact)
- `dim_plan` (Type 2 for plan changes)
- `fct_subscription_daily_snapshot` (periodic snapshot)

Common metrics:
- MRR
- Churn rate
- Net expansion

## Data Quality in Gold
Add tests for:
- Fact grain uniqueness
- Dimension key validity (FK coverage)
- Null thresholds for required business fields
- Reconciliation against source-of-truth totals

## Performance Patterns
- Partition facts by business date
- Cluster by common filter/join keys
- Pre-aggregate heavy dashboards into marts

## Common Mistakes
- Building one giant denormalized "gold" table for everything
- Embedding conflicting KPI definitions across teams
- Skipping conformed dimensions and semantic ownership

## Practical Checklist
1. Grain and KPI dictionary approved by stakeholders.
2. Conformed dimensions reused, not duplicated.
3. SCD policy documented for mutable attributes.
4. Gold refresh dependencies and SLAs documented.

## Related Notes
- [[kimball-principles]]
- [[medallion-architecture]]
