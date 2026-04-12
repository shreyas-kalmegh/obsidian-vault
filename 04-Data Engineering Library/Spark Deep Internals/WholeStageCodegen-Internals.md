# WholeStageCodegen Internals

## Overview
Whole-stage code generation is a Spark SQL optimization that fuses multiple physical operators and expressions into a single block of generated JVM code. Instead of moving each row through many virtual-function calls and object-heavy operator layers, Spark generates tighter loops that process data in a more CPU-efficient way.

High-level idea:
- normal execution can involve many operator boundaries and per-row overhead
- whole-stage codegen combines compatible operators into a single generated pipeline
- Spark compiles that generated Java code and executes the fused path
- fewer abstractions in the hot path usually means better CPU efficiency

Why it matters:
- it is one of the main reasons Spark SQL can be much faster than naive row-by-row execution
- it reduces function-call overhead, branching overhead, and object churn
- when codegen is disabled or broken by plan shape, query performance often drops noticeably

Interview-safe line:
- "Whole-stage codegen speeds Spark up by fusing compatible operators into generated Java code so rows flow through tight loops instead of many interpreted operator calls."

## Where Whole-Stage Codegen Fits
Whole-stage codegen is a physical execution optimization, not a logical optimization.

Execution flow at a high level:
1. Catalyst optimizes the logical plan.
2. Spark chooses a physical plan.
3. Compatible physical operators are grouped into codegen stages.
4. Spark generates Java source for those stages.
5. The JVM compiles and runs the generated code.

Important distinction:
- Catalyst simplifies the plan logically
- whole-stage codegen makes the physical execution path cheaper on the CPU

## What Gets Fused
Whole-stage codegen works best when Spark can combine a chain of row-based operators into one pipeline.

Typical candidates include:
- projections
- filters
- some aggregations
- some join paths
- expression evaluation around row processing

Example mental model:
- without fusion: scan -> filter -> project -> aggregate as separate layers
- with fusion: one generated loop evaluates filter, computes projected columns, and updates aggregation state inline

Why this helps:
- fewer intermediate row objects
- fewer iterator and method-call boundaries
- better JVM optimization opportunities

## Codegen Pipeline Structure
Spark groups compatible operators into a "whole-stage codegen subtree." Inside that subtree, generated code often follows a pattern like:
1. read row or unsafe row input
2. evaluate filter predicates
3. compute expressions
4. update aggregation/join state or emit output

The generated code is specialized for the query plan:
- exact expressions are embedded directly
- null checks are tailored to used columns
- data access paths are optimized for the expected schema

This specialization is a major reason generated execution is faster than a generic operator framework.

## Expression Fusion
Expression fusion means Spark combines multiple expression evaluations into one generated method or code path instead of evaluating each expression through separate interpreted layers.

Examples:
- arithmetic expressions
- `CASE WHEN` logic
- null checks
- cast operations
- predicate evaluation

Why it matters:
- removes repeated expression dispatch overhead
- reduces temporary object creation
- allows the JVM to optimize a larger contiguous hot path

Practical takeaway:
- built-in Spark SQL functions benefit much more from codegen than opaque UDF logic

## Relationship with Tungsten
Whole-stage codegen and Tungsten are closely related but not identical.

Useful mental model:
- Tungsten focuses on efficient memory layout and low-level execution efficiency
- whole-stage codegen focuses on generating fast CPU execution paths

Together they enable:
- `UnsafeRow`-oriented processing
- reduced object allocation
- efficient in-memory access patterns
- fast row-based operator pipelines

Interview-safe line:
- "Tungsten improves memory and binary layout; whole-stage codegen improves how Spark executes the row-processing loop."

## UnsafeRow and Tight Loops
Whole-stage codegen often operates over `UnsafeRow` or similarly efficient internal binary representations rather than rich JVM objects.

Benefits:
- compact memory representation
- lower GC pressure
- faster field access in generated code

Why it matters:
- codegen gains are strongest when Spark stays in efficient internal formats
- repeated conversion to higher-level objects reduces those gains

## Pipeline Boundaries
Not every operator can participate in the same fused stage. Some operators naturally break the pipeline.

Common boundaries include:
- shuffle exchanges
- sort boundaries
- row/columnar conversion boundaries
- operators without codegen support
- Python UDF paths

Mental model:
- whole-stage codegen is powerful inside a compatible segment
- data movement and unsupported operators split the plan into multiple segments

## Fallback Scenarios
Spark cannot always use whole-stage codegen end to end.

Common reasons for fallback:
- unsupported physical operator
- Python UDF or external language boundary
- code becomes too large or complex to generate/compile cleanly
- plan segment runs in columnar mode instead of row-codegen path
- certain complex expressions or nested structures reduce codegen effectiveness

What fallback means:
- Spark may execute part of the plan with codegen and another part without it
- performance is often still acceptable, but hot paths may become slower

Practical rule:
- one unsupported operator can break an otherwise efficient fused pipeline

## Code Size and Compilation Tradeoffs
Generated code is not free.

Potential costs:
- Java source generation time
- JVM compilation time
- oversized generated methods can become hard for the JVM to optimize
- very complex plans can lead to method splitting or reduced codegen benefit

Why this matters:
- codegen usually helps steady-state execution
- for very small jobs, compile overhead may not matter much either way
- for complex plans, excessive expression complexity can reduce the expected gains

## Whole-Stage Codegen vs Columnar Execution
Whole-stage codegen mainly optimizes row-based JVM pipelines. Columnar execution optimizes batch-oriented processing, often for Parquet/ORC scans and vectorized operators.

Key difference:
- whole-stage codegen: row-based, generated Java hot loops
- columnar execution: batch-based, vectorized processing

Modern Spark plans may use both in different segments.

Practical takeaway:
- these are complementary optimizations, not strict competitors
- repeated transitions between row and columnar paths can reduce benefits

## Performance Impact

### Where it helps most
- filter-heavy SQL workloads
- projection-heavy transformations
- aggregation pipelines with built-in expressions
- row-based join and aggregation paths without heavy UDF usage

### Why it improves performance
- fewer virtual calls
- less iterator overhead
- less object allocation
- better CPU cache behavior
- more opportunities for JVM optimization

### Symptoms when it is helping
- faster per-task CPU processing
- lower overhead for expression-heavy plans
- better throughput on built-in SQL/DataFrame operations

## Common Reasons You Lose Codegen Benefits
- Python UDFs
- Scala/Java UDF-heavy plans compared with built-in expressions
- unsupported operators in critical path
- too many row/column conversions
- very complex expressions that trigger codegen fragmentation or fallback

Practical rule:
- If performance matters, prefer native Spark SQL functions over UDFs whenever possible

## What to Look for in Plans
In `explain()` output, Spark often marks fused segments with codegen-related indicators such as whole-stage codegen subtrees.

Useful signs:
- operators grouped into a codegen stage
- fewer breaks between filter/project/aggregate paths
- row-based operators staying within the same subtree

Warning signs:
- unexpected pipeline breaks
- UDF-heavy segments
- repeated row/column transitions

## Debugging Checklist
1. Inspect the physical plan and note whole-stage codegen subtrees.
2. Identify where the pipeline breaks.
3. Look for UDFs or unsupported operators in the hot path.
4. Compare row-based and columnar boundaries if performance is inconsistent.
5. Prefer built-in expressions before tuning low-level configs.
6. If needed, compare behavior with codegen-related settings for diagnosis rather than as a first fix.

## Config Knobs to Know
Common context-dependent settings include:
- `spark.sql.codegen.wholeStage`
- `spark.sql.codegen.factoryMode`
- `spark.sql.shuffle.partitions` indirectly, because plan shape affects stage structure

Guideline:
- do not start by toggling codegen off
- first understand whether the plan shape is preventing effective fusion

## Interview Angle

### Good concise answer
- "Whole-stage codegen generates fused Java code for compatible Spark SQL operators so rows are processed in tight loops with less per-row overhead."

### Stronger follow-up answer
- "Its biggest benefit is reducing interpretation and object overhead across chains like filter -> project -> aggregate, but it breaks at shuffle boundaries, UDFs, unsupported operators, and some row/column transitions."

## Why It Matters
Understanding whole-stage codegen helps you:
- explain why native Spark SQL expressions are much faster than many UDF-heavy pipelines
- diagnose when a physical plan is CPU-bound rather than network-bound
- recognize why operator fusion disappeared in a plan
- connect Tungsten, `UnsafeRow`, and generated execution into one mental model

## Related
- [[04-Data Engineering Library/Spark Deep Internals/Columnar-Execution-Engine.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Catalyst-Optimizer-Rule-Catalog.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Performance-Tuning-Guide.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Tungsten-Memory-Management.md]]
