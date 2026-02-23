# Surrogate vs Natural Keys

## Natural Key
- Business-generated identifier (e.g., customer_id from source).
- May change, collide across systems, or be reused.

## Surrogate Key
- Warehouse-generated stable key.
- Enables SCD and source-system decoupling.

## Senior-Level Practice
Use natural keys for business matching and surrogate keys for dimensional joins.

## Checklist
- [ ] Natural key uniqueness tested per source
- [ ] Surrogate key generation deterministic and documented
- [ ] Key mapping lineage retained

## Common Mistakes
- Using mutable natural keys as dimension PK
- Dropping key mapping history

## Interview Prompts
- Why not use natural keys directly in fact joins?

## Related Notes
- [[scd-types]]
- [[conformed-dimensions]]
