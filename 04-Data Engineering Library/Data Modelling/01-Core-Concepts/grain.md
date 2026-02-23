# Grain

## Definition
Grain is the exact level of detail represented by one row in a fact table.

## Why It Matters
- Drives fact table design, dimensional keys, and metric correctness.
- Prevents duplicate counting and ambiguous metrics.

## Practical Rule
Declare grain in one sentence before writing schema.
Example: "One row per order line item at time of purchase."

## Checklist
- [ ] Grain statement written explicitly
- [ ] Every measure aligned to that grain
- [ ] Dimensions compatible with that grain

## Common Mistakes
- Changing grain later without model migration plan
- Mixing event-level and snapshot-level measures in one fact

## Interview Prompts
- How do you model multiple grains in one domain?

## Related Notes
- [[facts-vs-dimensions]]
- [[fact-table-types]]
