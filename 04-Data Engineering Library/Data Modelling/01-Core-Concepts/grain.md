# Grain

## Overview
Grain is the exact meaning of one row in a fact table.
If grain is ambiguous, metrics will be wrong.

## Grain Statement
Write grain as a single explicit sentence before schema design.

Examples:
- "One row per order line at purchase time."
- "One row per account per day end-of-day snapshot."
- "One row per claim from submission to settlement lifecycle."

## Why Grain Matters
Grain determines:
- Which measures are valid
- Which dimensions can join safely
- Whether updates or inserts are expected
- How duplicates are detected

## Good vs Bad Design
Good:
- `fct_order_line` at line grain with `quantity`, `unit_price`, `discount_amount`

Bad:
- Mixing order-line metrics and monthly account balance in same fact

## Example: Metric Correctness
If grain is order line, `SUM(net_amount)` is valid revenue.
If grain is order header, that same sum can double-count when joined to product lines.

## SQL Example
```sql
-- Grain: one row per order line
SELECT
  order_id,
  SUM(net_amount) AS order_revenue
FROM fct_order_line
GROUP BY order_id;
```

## Multi-Grain Strategy
Do not force multiple grains into one fact.
Use separate facts:
- `fct_order_line` (event detail)
- `fct_order_daily_snapshot` (periodic status)

## Practical Checklist
1. Write grain statement in model doc.
2. Validate every measure against grain.
3. Validate every dimension join against grain.
4. Add uniqueness tests matching grain keys.

## Related Notes
- [[facts-vs-dimensions]]
- [[fact-table-types]]
