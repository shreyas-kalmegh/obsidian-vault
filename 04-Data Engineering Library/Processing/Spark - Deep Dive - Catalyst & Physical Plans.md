# Spark Deep Dive — Catalyst Optimizer & Physical Plans

## Overview
Catalyst translates a high-level query (DataFrame/Dataset) to optimized physical plans. Understanding its stages helps reason about performance.

## Phases
1. Logical plan creation: user API -> unresolved logical plan.
2. Analysis: resolves attribute references using catalog and schemas.
3. Optimization: rule-based (and cost-based in newer versions) optimizations applied.
4. Physical planning: generate one or more physical plans.
5. Code generation (WholeStageCodegen) and execution.

## Important optimizations
- Predicate pushdown: filters moved closer to data source.
- Projection pruning: read fewer columns.
- Constant folding and null propagation.
- Join reorder and broadcast join selection (using statistics).

## WholeStageCodegen
- Fuse many physical operators into a single generated Java method to reduce virtual calls and object overhead.
- Works best when operators can be expressed in codegen-friendly form.

## Practical tips
- Use `explain(true)` to view QueryExecution stages and physical plan details.
- For UDFs, prefer vectorized UDFs (Pandas UDFs) or avoid row-at-a-time UDFs where possible.
- Monitor `WholeStageCodegen` disabled warnings — complex queries may disable it, impacting performance.
