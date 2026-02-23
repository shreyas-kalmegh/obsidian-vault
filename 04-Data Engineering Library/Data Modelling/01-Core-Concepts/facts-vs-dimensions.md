# Facts vs Dimensions

## Facts
- Store measurable business events.
- Usually numeric and aggregatable.
- Link to dimensions via foreign keys.

## Dimensions
- Store descriptive context for slicing/filtering facts.
- Include business attributes and hierarchies.
- Often include surrogate keys and SCD behavior.

## Rule of Thumb
If it answers "how much/how many", it is usually a fact.
If it answers "by what/who/where/which", it is usually a dimension.

## Checklist
- [ ] Facts contain measurable metrics
- [ ] Dimensions contain descriptive attributes
- [ ] FK relationships are explicit and validated

## Common Mistakes
- Storing descriptive text in facts
- Keeping volatile metrics in dimensions

## Interview Prompts
- Can a table be both fact and dimension?

## Related Notes
- [[grain]]
- [[surrogate-vs-natural-keys]]
