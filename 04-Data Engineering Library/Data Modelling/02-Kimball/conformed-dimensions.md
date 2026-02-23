# Conformed Dimensions

## Definition
Shared dimensions reused across multiple facts/marts with consistent semantics.

## Why Important
- Enables cross-domain metrics consistency.
- Supports enterprise-level reporting.

## Example
`dim_customer` shared by `fct_orders`, `fct_support_tickets`, and `fct_payments`.

## Checklist
- [ ] Attribute definitions standardized
- [ ] Key mapping unified across marts
- [ ] Versioning policy documented

## Common Mistakes
- Duplicate customer dimensions with slightly different logic
- Same attribute names with different meaning

## Interview Prompts
- How do conformed dimensions reduce metric disputes?

## Related Notes
- [[kimball-principles]]
- [[bus-matrix]]
