# Bus Matrix

## Purpose
Maps business processes (facts) to conformed dimensions.

## Template
| Business Process | Fact Table | Customer | Product | Date | Channel | Geography |
|---|---|---|---|---|---|---|
| Order | fct_orders | Y | Y | Y | Y | Y |
| Return | fct_returns | Y | Y | Y | Y | Y |
| Payment | fct_payments | Y | N | Y | Y | Y |

## Checklist
- [ ] Every fact mapped to dimensions
- [ ] Shared dimensions identified
- [ ] Gaps and duplicate dims removed

## Common Mistakes
- Building marts without cross-domain map
- Ignoring slowly changing conformed dims

## Interview Prompts
- How do you use bus matrix for delivery sequencing?

## Related Notes
- [[conformed-dimensions]]
- [[kimball-principles]]
