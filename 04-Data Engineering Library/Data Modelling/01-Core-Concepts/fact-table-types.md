# Fact Table Types

## Transaction Fact
- One row per business event (e.g., order line, click, payment).
- Best for detailed analysis and drill-down.

## Periodic Snapshot Fact
- One row per entity per fixed interval (e.g., daily account balance).
- Good for trend reporting.

## Accumulating Snapshot Fact
- One row per lifecycle entity, updated as milestones occur.
- Good for pipeline/flow duration analysis.

## Choose By Question Pattern
- Event analysis -> Transaction
- Time-series status -> Periodic Snapshot
- Process milestone tracking -> Accumulating Snapshot

## Checklist
- [ ] Fact type chosen from query patterns
- [ ] Update strategy defined (append vs update)

## Common Mistakes
- Using transaction fact for all use cases
- Updating append-only historical facts without audit strategy

## Interview Prompts
- Why choose accumulating snapshot for order fulfillment?

## Related Notes
- [[grain]]
- [[scd-types]]
