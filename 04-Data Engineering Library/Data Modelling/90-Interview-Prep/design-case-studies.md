# Design Case Studies

## Overview
Case studies test end-to-end design thinking under business constraints.
A strong answer is structured, explicit on tradeoffs, and implementation-aware.

## Reusable Case Study Template
1. Business problem and KPI definitions
2. SLA and freshness requirements
3. Source systems and constraints (CDC, retention, data quality)
4. Grain-first model proposal (facts, dimensions, SCD)
5. Incremental/backfill strategy
6. Data quality and reconciliation tests
7. Performance/cost plan
8. Risks and mitigation

## Case 1: Subscription Analytics
Problem:
- Track MRR, churn, expansion by plan, region, and cohort

Model:
- Facts:
  - `fct_subscription_event` (transaction)
  - `fct_subscription_daily_snapshot` (periodic)
- Dimensions:
  - `dim_customer` (Type 2 for segment/tier)
  - `dim_plan` (Type 2 for plan metadata changes)
  - `dim_date`

Key tradeoff:
- Transaction-only model is flexible but expensive for daily reporting.
- Add snapshot fact for predictable dashboard performance.

## Case 2: Marketplace Commissions
Problem:
- Compute net commission after refunds, promos, and chargebacks

Model:
- `fct_order_line`
- `fct_refund_line`
- `fct_chargeback`
- Conformed `dim_seller`, `dim_product`, `dim_date`

Important detail:
- Keep commission policy version in dimension or policy bridge to support historical policy changes.

## Case 3: Fraud Feature Store + BI Layer
Problem:
- Near-real-time fraud features plus trusted daily risk reporting

Model split:
- Feature layer: event-level Silver/feature tables (low latency)
- BI Gold layer: curated risk facts by day/account/channel

Tradeoff to explain:
- Feature freshness vs BI consistency and reproducibility

## Interview Delivery Format (5-7 minutes)
1. Clarify assumptions and SLA.
2. State grain for each fact.
3. Show dimension and SCD choices.
4. Explain incremental logic and replay plan.
5. Cover testing and rollback.

## Example Validation Set
- Grain uniqueness tests (`order_id`, `order_line_id`)
- FK coverage to conformed dimensions
- Reconciliation with source totals
- Late-arrival correction impact checks

## Common Mistakes in Case Study Answers
- Jumping into tools before modeling
- Skipping SLA and data contract constraints
- Proposing "one table for everything"
- Ignoring failure/recovery/backfill behavior

## Practical Checklist
1. Include one-page architecture/data-flow view.
2. Explicitly list grain statements.
3. Call out at least one tradeoff with alternatives.
4. Include operational recovery plan.

## Related Notes
- [[scenario-questions]]
- [[kimball-principles]]
- [[medallion-architecture]]
