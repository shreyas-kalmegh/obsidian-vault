# Catalyst Optimizer Rule Catalog

## Overview
Catalyst is Spark SQL's rule-based query optimization framework. After SQL/DataFrame operations are parsed into a logical plan and analyzed, Catalyst applies batches of optimizer rules that rewrite the plan into a semantically equivalent but cheaper shape.

High-level idea:
- Input plan: correct but not necessarily efficient logical plan
- Optimizer: applies rewrite rules in batches until fixpoint or batch limit
- Output plan: leaner logical plan that is easier for the planner to turn into an efficient physical execution strategy

Important distinction:
- Catalyst optimizer rules operate on the logical plan
- The cost-based/planning side later chooses physical operators like broadcast hash join or sort merge join

## Where the Optimizer Fits
1. Parser creates an unresolved logical plan.
2. Analyzer resolves table names, columns, data types, and functions.
3. Optimizer rewrites the analyzed logical plan using rule batches.
4. Planner chooses candidate physical plans.
5. Spark selects a physical plan and executes it.

Interview-safe line:
- "Catalyst first makes the query logically cleaner and cheaper, then the planner decides how to execute that optimized plan physically."

## How Rules Are Applied
- Rules are grouped into batches such as operator optimization, constant folding, or join-focused rewrites.
- Many batches run to a fixpoint, meaning Spark reapplies the rules until the plan stops changing or a batch iteration cap is reached.
- Rules are pattern-based tree transformations. They match nodes in the logical plan and replace them with equivalent forms.

Why fixpoint matters:
- One rewrite often enables another.
- Example: constant folding may simplify a filter predicate, which then allows boolean simplification or filter elimination.

## High-Value Rule Categories

### 1) Constant Folding
Spark evaluates deterministic constant expressions during optimization instead of at runtime.

Example:
```sql
SELECT * FROM sales WHERE price > 100 * 2
```
becomes conceptually:
```sql
SELECT * FROM sales WHERE price > 200
```

Why it helps:
- Less expression work per row
- Simpler predicates enable later rewrites

### 2) Constant Propagation and Null Simplification
Catalyst propagates known values and rewrites expressions involving `NULL` when semantics are clear.

Examples:
- `x = 5 AND x + 1 > 3` can be partially simplified
- `col IS NOT NULL AND col + 1 > 10` may allow safer downstream reasoning

Why it helps:
- Reduces redundant expression evaluation
- Produces simpler plans for later phases

### 3) Predicate Pushdown
Filters are moved as close to the data source as semantics allow.

Example logical rewrite:
- Bad shape: scan full dataset, then filter
- Better shape: push filter beneath projection/join where valid, ideally into the datasource scan

Example:
```sql
SELECT user_id FROM events WHERE event_date = '2026-04-01'
```

Benefits:
- Less data read from storage
- Less shuffle/network cost later
- Better partition pruning and file skipping

Important nuance:
- Catalyst can push predicates down in the logical plan, but actual datasource pushdown depends on source capabilities.

### 4) Projection Pruning
Unused columns are removed early from the plan.

Example:
```sql
SELECT user_id FROM events
```
should not force Spark to carry all columns if only `user_id` is needed.

Why it matters:
- Fewer columns decoded from Parquet/ORC
- Lower memory pressure
- Smaller shuffle payloads

Practical takeaway:
- Column pruning is one of the biggest reasons Spark performs well on columnar formats.

### 5) Boolean Expression Simplification
Catalyst simplifies redundant or tautological predicates.

Examples:
- `a = 1 AND true` -> `a = 1`
- `a = 1 OR false` -> `a = 1`
- duplicate predicates may be collapsed

Why it helps:
- Cleaner expression trees
- Less CPU spent evaluating unnecessary conditions

### 6) Combine and Collapse Adjacent Operators
Catalyst merges adjacent filters, projects, and other compatible operators.

Examples:
- multiple `Filter` nodes become one
- chained `Project` nodes are collapsed when safe

Why it matters:
- Shorter plans
- Lower expression overhead
- Easier for later planning/codegen optimizations

### 7) Reorder and Simplify Joins
Catalyst applies join rewrites and, when statistics are available, may support cost-based join reordering.

Typical goals:
- expose better join structure
- eliminate unnecessary joins
- reorder inner joins to reduce intermediate data volume

Important nuance:
- Pure rule-based optimization does structural rewrites
- true join reordering quality improves when table statistics are available

### 8) Eliminate Redundant Work
Catalyst removes operators that do not affect the result.

Examples:
- unnecessary projections
- redundant sorting in some contexts
- filters that are always true

Why it helps:
- Less CPU and memory work
- Cleaner plan for physical strategy selection

## Common Rule Families to Recognize

### Pushdown and pruning family
- predicate pushdown
- projection/column pruning
- partition pruning

This family reduces data volume as early as possible.

### Expression simplification family
- constant folding
- boolean simplification
- null propagation
- common expression cleanup

This family reduces per-row compute overhead.

### Structural cleanup family
- collapse project
- combine filters
- eliminate no-op operators

This family makes the logical plan smaller and easier to optimize further.

### Join-focused family
- join reordering
- predicate inference around joins
- outer join simplifications when semantics allow

This family has outsized impact because joins often dominate Spark job cost.

## Example Plan Rewrite Flow
Suppose the query is:

```sql
SELECT customer_id
FROM orders
WHERE order_status = 'COMPLETE'
  AND 1 = 1
```

Catalyst may conceptually do the following:
1. Remove `1 = 1` via constant/boolean simplification.
2. Prune all columns except `customer_id` and `order_status`.
3. Push `order_status = 'COMPLETE'` toward the scan.
4. Hand a much smaller logical plan to the physical planner.

Result:
- less file data scanned
- fewer columns decoded
- less memory moved through the pipeline

## Rule-Based vs Cost-Based Thinking
Catalyst is often described as rule-based, but Spark also has cost-informed behavior in selected areas.

Useful mental model:
- Rule-based optimization: "This rewrite is always or usually safe and beneficial."
- Cost-based optimization: "Among valid alternatives, choose the cheapest using stats."

Examples:
- Constant folding is straightforwardly rule-based.
- Join reordering and join strategy selection become better with row-count and size statistics.

## What Engineers Should Look for in Practice

### In `explain()` output
- filters close to scans
- fewer projected columns
- simpler expressions
- reduced operator nesting

### In data source behavior
- pushed filters shown in scan metadata
- partition pruning visible in plan or scan details
- vectorized reads preserved when only needed columns are read

### In performance symptoms
- large scan size despite selective filters often means pushdown/pruning failed
- wide shuffles may indicate poor projection pruning
- expensive joins may indicate missing stats or suboptimal join ordering

## Common Reasons Optimizations Do Not Help
- Python UDFs or opaque expressions block Catalyst visibility
- datasource cannot support pushed predicates
- table statistics are missing or stale
- expressions are non-deterministic, so Spark cannot safely rewrite them
- query shape forces semantics that prevent aggressive pushdown or reordering

Practical rule:
- Built-in Spark SQL expressions are far more optimizer-friendly than custom UDF-heavy logic

## Debugging Checklist
1. Run `df.explain("formatted")` or SQL `EXPLAIN EXTENDED`.
2. Check whether filters appear near the scan.
3. Confirm only required columns are being read.
4. Look for unnecessary projects, filters, or joins.
5. Verify table statistics if join ordering seems poor.
6. Replace UDF logic with native expressions when possible.

## Interview Angle

### Good concise answer
- "Catalyst applies rule-based transformations to the analyzed logical plan, such as constant folding, predicate pushdown, and column pruning, so Spark reads less data and does less work before choosing a physical execution strategy."

### Stronger follow-up answer
- "The biggest wins usually come from reducing data early: push filters to scans, prune unused columns, simplify expressions, and avoid UDFs that hide intent from the optimizer."

## Why It Matters
Understanding Catalyst's rule catalog helps you:
- explain why two equivalent queries can produce very different execution costs
- diagnose why filter pushdown or pruning did not occur
- design DataFrame/SQL code that the optimizer can reason about effectively
- separate logical-plan issues from physical-plan issues during tuning

## Related
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Architecture-Overview.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Columnar-Execution-Engine.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Performance-Tuning-Guide.md]]
