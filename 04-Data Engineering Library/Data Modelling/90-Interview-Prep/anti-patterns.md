# Anti-Patterns

## Overview
Interviewers often test whether you can recognize modeling failures and fix them incrementally without breaking reporting.
A strong answer includes:
1. Symptom
2. Root cause
3. Migration path

## Common Anti-Patterns and How to Respond

## 1) Undefined Grain
Symptom:
- Metrics disagree across teams
- Duplicate counting after joins

Why it fails:
- No clear row-level contract for facts

Interview response pattern:
- State a grain sentence first
- Add uniqueness test on grain keys
- Refactor mixed-grain fact into separate facts

Example:
- Split `fct_orders_all` into `fct_order_line` (transaction) and `fct_order_daily_snapshot` (periodic)

## 2) One Giant Wide Table for All Analytics
Symptom:
- Slow queries, confusing semantics, conflicting metric logic

Why it fails:
- Combines unrelated grains and use cases

Interview response pattern:
- Move to dimensional model (facts + conformed dimensions)
- Keep domain marts focused
- Preserve wide table temporarily for backward compatibility during migration

## 3) Type 2 Everywhere
Symptom:
- Exploding dimension row counts
- Complex joins for attributes that do not need history

Why it fails:
- Over-applies historical tracking

Interview response pattern:
- Choose SCD per attribute:
  - Type 1 for corrections/non-historical attributes
  - Type 2 for analytically significant historical attributes

Example:
- `customer_email` Type 1
- `customer_tier` Type 2

## 4) No Conformed Dimensions
Symptom:
- Same KPI gives different answers across marts

Why it fails:
- Shared entities are modeled with different definitions/keys

Interview response pattern:
- Introduce bus matrix
- Define canonical conformed dimensions (`dim_customer`, `dim_date`)
- Migrate marts in priority order

## 5) Metric Definitions Duplicated per Dashboard
Symptom:
- "Revenue" differs by dashboard/team

Why it fails:
- Metric logic is embedded in BI tools instead of governed model/semantic layer

Interview response pattern:
- Centralize metric definitions
- Add versioned metric contracts
- Backfill and reconcile historical differences

## 6) No Backfill or Replay Strategy
Symptom:
- Late data and incident recovery require manual ad hoc scripts

Why it fails:
- Pipeline is not reproducible

Interview response pattern:
- Keep replayable Bronze history
- Define deterministic reprocessing windows
- Add runbook for late-arrival corrections

## 7) No Ownership or Lineage
Symptom:
- Nobody knows who owns a broken KPI

Why it fails:
- Missing governance model

Interview response pattern:
- Define owner per table/metric
- Track lineage from source -> Silver -> Gold
- Add data quality SLAs and escalation paths

## Rapid Interview Framework
When asked to debug bad model design, answer in this order:
1. Clarify business question and SLA.
2. Identify grain and key anti-pattern.
3. Propose minimal viable fix first.
4. Describe phased migration and rollback plan.
5. Add tests and ownership controls.

## Practical Checklist
1. Can identify anti-pattern quickly from symptoms.
2. Can explain why it fails technically.
3. Can propose low-risk migration path.
4. Can name validation checks after fix.

## Related Notes
- [[scenario-questions]]
- [[performance-and-cost]]
- [[kimball-principles]]
