# Data Vault vs Kimball

## Kimball
- Fast analytics consumption
- Business-process-oriented marts
- Great for BI and metric-serving

## Data Vault
- Auditability and source traceability focus
- Hubs, links, satellites pattern
- Useful for high-change integration layers

## Practical Position
Many modern teams use Data Vault/integration patterns upstream and Kimball/star outputs for consumption.

## Checklist
- [ ] Chosen pattern tied to business need
- [ ] Audit and latency requirements considered

## Common Mistakes
- Treating Data Vault as a BI serving model
- Ignoring consumption performance

## Interview Prompts
- When would you adopt Data Vault in a lakehouse?

## Related Notes
- [[kimball-principles]]
- [[governance-and-lineage]]
