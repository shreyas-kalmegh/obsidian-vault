# Fact Table Types

## Overview
Choose fact type based on business questions and process behavior.
Most domains use more than one fact type.

## 1) Transaction Fact
One row per business event.

Use when you need:
- Detailed analysis and drill-through
- Flexible aggregations
- Event-level auditability

Example:
- `fct_order_line` with one row per item purchased

## 2) Periodic Snapshot Fact
One row per entity per fixed interval (day/week/month).

Use when you need:
- Trends over consistent time buckets
- Fast reporting without expensive event recomputation

Example:
- `fct_account_daily_balance` with one row per account per day

## 3) Accumulating Snapshot Fact
One row per lifecycle object, updated as milestones occur.

Use when you need:
- Funnel and cycle-time analytics
- SLA stage duration tracking

Example:
- `fct_claim_lifecycle` with `submitted_ts`, `approved_ts`, `paid_ts`

## Comparison
- Transaction: append-heavy, largest volume, maximum detail
- Periodic snapshot: predictable size, trend-friendly
- Accumulating snapshot: update-heavy, lifecycle-focused

## Example Decision
E-commerce domain:
- Revenue and product mix -> transaction fact (`fct_order_line`)
- Daily inventory levels -> periodic snapshot (`fct_inventory_daily`)
- Fulfillment lead time -> accumulating snapshot (`fct_fulfillment_cycle`)

## Common Mistakes
- Using only transaction facts for all use cases
- Building accumulating snapshot without reliable milestone timestamps
- Creating snapshots without clear interval contract

## Practical Checklist
1. Start from query patterns, not storage preference.
2. Document insert/update behavior.
3. Align partitioning and refresh strategy with fact type.

## Related Notes
- [[grain]]
- [[scd-types]]
