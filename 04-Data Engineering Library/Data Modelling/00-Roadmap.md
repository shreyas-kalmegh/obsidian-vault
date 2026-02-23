# Data Modelling Roadmap (Senior Data Engineer)

## Goal
Build practical mastery to design reliable, scalable analytical models for batch and near-real-time use cases.

## Priority Order
1. Core modelling foundations
2. Kimball dimensional modelling
3. Modern lakehouse modelling (Medallion + incremental)
4. Advanced architecture tradeoffs (Data Vault, semantic layer, governance)
5. Interview case-practice and anti-pattern recognition

## What to Learn First
- Start with [[grain]] and [[facts-vs-dimensions]].
- Then [[fact-table-types]] and [[scd-types]].
- Then [[kimball-principles]] and [[star-vs-snowflake]].
- Then [[medallion-architecture]] and [[gold-layer-dimensional-models]].

## 8-Week Plan
1. Week 1-2: Core concepts + SCD design drills
2. Week 3-4: Kimball + bus matrix + conformed dimensions
3. Week 5-6: Medallion + CDC + late-arriving data
4. Week 7: Performance/cost + governance/lineage
5. Week 8: Interview scenarios + design case studies

## Deliverables
- 3 end-to-end model designs from raw events to gold marts
- 1 conformed-dimension bus matrix
- 1 CDC + backfill design note
- 1 interview answer bank from [[scenario-questions]]

## Checklist
- [ ] Can define grain before selecting columns
- [ ] Can choose fact table type by use case
- [ ] Can justify SCD strategy and key design
- [ ] Can map Medallion layers to dimensional gold outputs
- [ ] Can explain star vs snowflake with performance tradeoffs

## Common Mistakes
- Modelling tables before deciding grain
- Treating all facts as additive
- Using Type 2 SCD everywhere without cost analysis
- Mixing raw and business-cleaned semantics in one table

## Interview Prompts
- Design a model for e-commerce orders and returns
- How would you handle late-arriving dimensions?
- Star vs snowflake for a high-concurrency BI workload

## Related Notes
- [[kimball-principles]]
- [[medallion-architecture]]
- [[performance-and-cost]]

## Navigation
- [[00-MOC]]
