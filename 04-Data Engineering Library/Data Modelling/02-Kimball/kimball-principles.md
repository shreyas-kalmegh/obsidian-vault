# Kimball Principles

## Core Ideas
- Model around business processes.
- Declare grain first.
- Build dimensional models (facts + dimensions).
- Deliver incrementally via data marts.

## Why It Works
- Query-friendly for analytics.
- Easy for BI tools and business users.
- Supports iterative domain expansion.

## Checklist
- [ ] Business process identified
- [ ] Grain declared
- [ ] Fact and conformed dimensions designed
- [ ] Incremental delivery plan defined

## Common Mistakes
- Skipping conformed dimensions
- Modelling source system structures directly

## Interview Prompts
- Explain a full Kimball design for orders domain.

## Related Notes
- [[bus-matrix]]
- [[star-vs-snowflake]]
