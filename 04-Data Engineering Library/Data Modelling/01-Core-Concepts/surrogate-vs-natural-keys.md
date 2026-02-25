# Surrogate vs Natural Keys

## Overview
Dimensional models usually use both key types:
- Natural key for business identity matching
- Surrogate key for warehouse joins and history handling

## Natural Key
Business-generated identifier from source systems.

Examples:
- `customer_id` from CRM
- `product_code` from ERP

Benefits:
- Business-recognizable
- Useful for reconciliation

Risks:
- Can be mutable or reused
- Can conflict across source systems

## Surrogate Key
Warehouse-generated stable key.

Examples:
- `customer_key BIGINT`
- `product_key BIGINT`

Benefits:
- Stable join behavior
- Supports Type 2 dimensions cleanly
- Decouples warehouse from source key volatility

## Example Pattern
`dim_customer`:
- PK: `customer_key` (surrogate)
- Business key: `customer_id` (natural)

`fct_order_line` stores `customer_key`, not `customer_id`.

## When Natural Key in Facts Is Acceptable
- Staging/Silver layers
- Event logs before dimensional conformance

In Gold dimensional marts, prefer surrogate FK joins.

## Common Mistakes
- Using mutable natural key as dimension PK
- Dropping key mapping lineage tables
- Re-keying facts without controlled backfill plan

## Practical Checklist
1. Keep natural key in dimensions for traceability.
2. Use surrogate key for fact joins.
3. Preserve key mapping history across source migrations.
4. Add uniqueness tests by natural key + SCD validity.

## Related Notes
- [[scd-types]]
- [[conformed-dimensions]]
