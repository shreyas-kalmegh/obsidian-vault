# Scenario Questions

## How to Use This Note
For each scenario, answer with:
1. Clarifying questions
2. Modeling decision (grain, facts, dims, SCD)
3. Incremental + recovery strategy
4. Validation checks and tradeoffs

## 1. E-commerce Orders Model
Question:
Design dimensions and facts for orders, returns, payments, and shipping.

Strong answer outline:
- Facts:
  - `fct_order_line` (grain: one row per order line)
  - `fct_return_line`
  - `fct_payment`
  - `fct_shipment_event` or accumulating snapshot for fulfillment lifecycle
- Conformed dimensions:
  - `dim_customer`, `dim_product`, `dim_date`, `dim_channel`, `dim_geography`
- SCD:
  - Type 2 for `customer_tier`, Type 1 for corrected name/email

## 2. Late-Arriving Data
Question:
How do you correct 30 days of delayed events without metric drift?

Strong answer outline:
- Define lateness SLA and impacted marts
- Reprocess rolling window (for example last 30 days)
- Use deterministic merge ordering (`source_changed_ts`)
- Rebuild dependent Gold aggregates and publish restatement notice
Production-level walkthrough:
- See [[late-arriving-file-production-example]] for full Bronze -> Silver SCD2 -> Gold Type 2 flow.
- It covers: new keys, current-row change, mid-history late change, no-op duplicates, deletes, and idempotent replay.
- In interview answers, explicitly state that late arrivals may require updating non-current intervals, not only current rows.

## 3. SCD Strategy
Question:
Which customer attributes should be Type 1 vs Type 2?

Strong answer outline:
- Type 2: segmentation/tier/region when historical analysis depends on time
- Type 1: typo corrections/non-analytic fields
- Mention one-current-row constraint and non-overlapping validity tests

## 4. Medallion + Gold Stability
Question:
How should Silver contracts be designed so Gold remains stable?

Strong answer outline:
- Silver contract includes canonical types, keys, CDC semantics, and dedup policy
- Gold does not consume raw Bronze directly
- Schema evolution handled with versioned contracts and compatibility tests

## 5. Performance Incident
Question:
Dashboard query regressed from 5s to 90s. How do you triage?

Strong answer outline:
- Check query plan changes, partition pruning, join strategy, data skew
- Validate recent model/schema changes
- Add targeted optimization (clustering, pre-aggregation, join rewrite)
- Confirm result correctness after optimization

## Bonus Questions to Practice
- When do you choose star vs snowflake in a lakehouse?
- How do you bootstrap history when Kafka retention is insufficient?
- How do you migrate from a wide legacy table to dimensional marts with low risk?

## Interview Tip: Tradeoff Language
Use explicit tradeoff framing:
- "Option A is faster to ship but weaker for history correctness."
- "Option B costs more compute but gives deterministic replay."

## Practical Checklist
1. Use grain-first language in every answer.
2. Mention one failure mode and mitigation.
3. Include testing + rollback approach.
4. Keep answer business-SLA anchored.

## Related Notes
- [[design-case-studies]]
- [[anti-patterns]]
- [[late-arriving-data]]
- [[late-arriving-file-production-example]]
