# Bus Matrix

## Overview
A bus matrix maps business processes (facts) to conformed dimensions.
It is the planning artifact that prevents siloed marts.

## Why It Matters
- Exposes shared dimensions early
- Helps sequence delivery by business impact
- Highlights missing conformance before implementation

## Example Bus Matrix
| Business Process | Fact Table | Customer | Product | Date | Channel | Geography | Promotion |
|---|---|---|---|---|---|---|---|
| Orders | `fct_order_line` | Y | Y | Y | Y | Y | Y |
| Returns | `fct_return_line` | Y | Y | Y | Y | Y | Y |
| Payments | `fct_payment` | Y | N | Y | Y | Y | N |
| Support Tickets | `fct_ticket` | Y | N | Y | Y | Y | N |

## How to Use It
1. List core processes and candidate facts.
2. Mark dimensions each process needs.
3. Identify dimensions with highest reuse (`Customer`, `Date`).
4. Standardize definitions and key strategy for those first.

## Delivery Sequencing Example
- Sprint 1: Orders mart with conformed `dim_customer`, `dim_date`
- Sprint 2: Returns mart reusing same customer/date keys
- Sprint 3: Payments mart reusing customer/date/channel

## Governance Value
Bus matrix also works as a communication contract between:
- Data engineering
- BI/analytics
- Domain owners

## Common Mistakes
- Treating matrix as one-time artifact and never updating it
- Declaring dimensions conformed without aligned attribute semantics
- Creating process-specific "customer" dimensions that drift

## Practical Checklist
1. Keep matrix versioned with model changes.
2. Add owner per process and per conformed dimension.
3. Use matrix in design reviews before new marts are approved.

## Related Notes
- [[kimball-principles]]
- [[conformed-dimensions]]
