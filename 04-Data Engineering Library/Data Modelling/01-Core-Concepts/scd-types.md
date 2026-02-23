# SCD Types (Dimensions)

## Type 1
Overwrite old value. No history.

## Type 2
Add new row with effective dates and current flag. Full history.

## Type 3
Keep current and previous values in separate columns. Limited history.

## Type 4
Store current in main dimension and history in separate history table.

## Type 6
Hybrid of Type 1 + Type 2 + Type 3.

## When to Use
- Type 1: data correction, low history value
- Type 2: regulatory/analytical history required
- Type 3: current vs prior comparison only
- Type 4: high-change history separated for performance
- Type 6: both full history and simplified current-state reporting

## Checklist
- [ ] SCD type chosen per attribute, not per table blindly
- [ ] Surrogate key policy documented
- [ ] Effective date logic and late-arrival strategy defined

## Common Mistakes
- Type 2 for all attributes
- Missing current-flag uniqueness guarantees

## Interview Prompts
- How do you handle late arriving dimension updates in Type 2?

## Related Notes
- [[surrogate-vs-natural-keys]]
- [[cdc-and-incremental-modeling]]
