# Late-Arriving Data

## Overview
Late-arriving data occurs when facts or dimensions arrive after their expected processing window.
If unmanaged, it causes KPI drift, broken joins, and inconsistent reporting.

## Types of Late Arrival
1. Late facts
- Event arrives after daily/weekly aggregate already computed

2. Late dimensions
- Dimension change arrives after fact was loaded
- Common with Type 2 dimensions

3. Out-of-order CDC updates
- Older change event arrives after newer version

## Handling Strategies
### Reprocess Window
- Recompute affected partitions (for example last 3 days)
- Simple and robust when cost is acceptable

### Incremental Correction
- Use `MERGE` with change ordering (`source_changed_ts`)
- Update only impacted records

### Suspense/Unknown Members
- Load fact with `unknown` dimension key when dimension missing
- Backfill foreign key once dimension arrives

## Example: Late Fact Correction
```sql
-- Rebuild impacted day for daily revenue
DELETE FROM gold.mart_revenue_daily
WHERE order_date = DATE '2026-02-20';

INSERT INTO gold.mart_revenue_daily
SELECT order_date, SUM(net_amount) AS revenue
FROM gold.fct_order_line
WHERE order_date = DATE '2026-02-20'
GROUP BY order_date;
```

## Example: Late Type 2 Dimension Update
If customer region change effective on `2026-02-10` arrives on `2026-02-15`:
- Insert/adjust Type 2 rows with corrected validity windows
- Recompute point-in-time facts or marts for affected dates

## Operational Practices
- Define late-arrival SLA (for example 95% within 2 hours, 99% within 24 hours)
- Maintain correction jobs and runbooks
- Track metric revisions after corrections

## Monitoring Signals
- Late event ratio by source
- Count of facts mapped to unknown dimension keys
- Number of corrected partitions per day

## Common Mistakes
- Treating late data as negligible without measuring impact
- Using load time instead of business effective time
- Correcting Silver but not rebuilding dependent Gold marts

## Practical Checklist
1. Document acceptable lateness windows per domain.
2. Implement reprocess or correction workflow.
3. Add lineage-based downstream impact rebuild.
4. Communicate metric restatements to consumers.

## Related Notes
- [[cdc-and-incremental-modeling]]
- [[gold-layer-dimensional-models]]
- [[scd-types]]
