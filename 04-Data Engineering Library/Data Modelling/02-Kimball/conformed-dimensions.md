# Conformed Dimensions

## Overview
A conformed dimension is shared across marts with consistent meaning, keys, and behavior.
It enables trustworthy cross-domain analysis.

## What Must Be Conformed
1. Business meaning
- `customer_status` must mean the same thing across orders and support marts

2. Keys
- Same surrogate key mapping policy for the shared entity

3. SCD behavior
- Same Type 1/Type 2 treatment for shared attributes

## Example
`dim_customer` used by:
- `fct_order_line`
- `fct_return_line`
- `fct_payment`

If Gold tier segmentation changes to Type 2, all marts consuming that attribute must align.

## Conformance Pattern
- Define canonical attribute list and definitions.
- Split local-only attributes into mini-dimensions if needed.
- Manage changes via versioned data contract.

## Example Problem Without Conformance
Orders mart uses "active customer = purchased in last 90 days".
Support mart uses "active customer = account not suspended".
A single dashboard comparing both becomes misleading.

## Common Mistakes
- Same dimension name with different logic
- Per-mart custom code for core shared attributes
- No owner for shared dimension governance

## Practical Checklist
1. Maintain canonical spec for each conformed dimension.
2. Enforce shared tests across marts.
3. Track breaking changes and migration plan.
4. Align semantic layer metrics to conformed definitions.

## Related Notes
- [[kimball-principles]]
- [[bus-matrix]]
