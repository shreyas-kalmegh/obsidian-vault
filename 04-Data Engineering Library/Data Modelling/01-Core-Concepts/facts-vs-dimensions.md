# Facts vs Dimensions

## Overview
A dimensional model separates data into:
- Facts: measurable business activity
- Dimensions: descriptive business context

This separation keeps analytics fast, understandable, and consistent.

## Facts
Facts represent events or states you want to aggregate.

Typical characteristics:
- Numeric metrics (`amount`, `quantity`, `duration_seconds`)
- Foreign keys to dimensions
- High row counts
- Usually append-heavy (depending on fact type)

Example (`fct_order_line`):
- `order_line_id`, `customer_key`, `product_key`, `date_key`, `quantity`, `net_amount`

## Dimensions
Dimensions provide filtering, grouping, and business meaning.

Typical characteristics:
- Descriptive attributes (`customer_tier`, `region`, `category`)
- Surrogate primary key in warehouse
- Lower row counts than facts
- May use SCD strategy for history

Example (`dim_customer`):
- `customer_key`, `customer_id`, `customer_name`, `country`, `tier`, `is_current`

## How to Classify a Column
- If analysts ask "how much/how many" -> likely fact measure
- If analysts ask "by who/where/what" -> likely dimension attribute
- If attribute changes over time and needs history -> dimension with SCD strategy

## Example Query
```sql
SELECT
  d.month,
  c.country,
  SUM(f.net_amount) AS revenue
FROM fct_order_line f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY d.month, c.country;
```

## Common Modeling Mistakes
- Putting volatile descriptive attributes in facts
- Storing additive metrics inside dimensions
- Joining facts directly on natural keys without dimensional conformance

## Practical Checklist
1. Declare fact grain first.
2. Keep facts mostly numeric + FK keys.
3. Keep business descriptors in dimensions.
4. Decide SCD type per mutable dimension attribute.

## Related Notes
- [[grain]]
- [[fact-table-types]]
- [[surrogate-vs-natural-keys]]
