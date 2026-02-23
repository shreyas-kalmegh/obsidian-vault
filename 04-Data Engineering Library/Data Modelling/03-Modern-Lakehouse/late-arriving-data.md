# Late-Arriving Data

## Problem
Events or dimensions arrive after their expected processing window.

## Strategies
- Reprocess affected partitions/windows
- Use effective dating and correction logic
- Maintain suspense records for missing dimensions

## Checklist
- [ ] Late-arrival SLA defined
- [ ] Backfill + correction workflow automated
- [ ] Downstream metric impact monitored

## Common Mistakes
- Ignoring late data in daily aggregates
- No reconciliation process between source and warehouse

## Interview Prompts
- How do you handle late-arriving dimensions in Type 2 SCD?

## Related Notes
- [[cdc-and-incremental-modeling]]
- [[gold-layer-dimensional-models]]
