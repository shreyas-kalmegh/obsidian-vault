# Governance and Lineage

## Why It Matters
Senior engineers must ensure trust, compliance, and impact visibility for model changes.

## Core Practices
- Data contracts with producers
- Column-level lineage for key metrics
- PII classification and masking policies
- Audit trails for model changes

## Checklist
- [ ] Data owners and stewards documented
- [ ] Lineage available from source to dashboard
- [ ] PII controls enforced in models

## Common Mistakes
- No ownership for critical dimensions
- Untracked schema changes breaking downstream marts

## Interview Prompts
- How do you roll out a breaking model change safely?

## Related Notes
- [[semantic-layer]]
- [[data-vault-vs-kimball]]
