# Columnar Execution Engine

## Overview
Spark's columnar execution path processes data in `ColumnarBatch` format (multiple rows per batch, data laid out by column) instead of one row object at a time. This reduces CPU overhead, improves cache locality, and enables vectorized operators.

High-level idea:
- Row execution: per-row object processing, higher function-call/object overhead
- Columnar execution: per-batch vector processing, tighter loops, better memory efficiency

## Execution Path (Simplified)
1. Scan reads data source (Parquet/ORC commonly) into column vectors.
2. Spark forms `ColumnarBatch` objects.
3. Supported operators consume/produce batches.
4. If an unsupported operator appears, Spark inserts row/column conversion and continues in row path for that segment.

Why this matters:
- Conversions (`ColumnarToRow` / `RowToColumnar`) add overhead and can reduce gains from vectorization.

## Core Building Blocks

### 1) Column Vectors
- Each column is stored in a contiguous vector-like structure.
- Nullability often represented via bitset/null mask.
- Encoding/compression in source files (like Parquet) is decoded into vectors for compute.

### 2) ColumnarBatch
- Logical unit: N rows x M columns.
- Operators work on batches, amortizing overhead across many rows.
- Batch size affects memory footprint and CPU efficiency tradeoff.

### 3) Vectorized Reader
- Parquet/ORC readers can decode entire chunks into vectors.
- Best performance when queries select fewer columns and push filters early.

## Operator Support and Fallback
Columnar execution is strongest when the full path stays columnar.

Common reasons for fallback to row path:
- Python UDF-heavy logic
- Unsupported expressions/operators for columnar backend
- Certain custom datasource behaviors

Plan indicators to watch:
- Good sign: more columnar operators, fewer conversions
- Warning sign: repeated `ColumnarToRow` and `RowToColumnar` transitions

## Relationship with WholeStageCodegen
- WholeStageCodegen mainly optimizes JVM row-based pipelines by generating fused Java code.
- Columnar execution optimizes via vectorized batch processing.
- In modern Spark plans, you may see a mix: some segments codegen row-based, others run columnar.

Interview-safe line:
- "Columnar and WholeStageCodegen are complementary optimizations; best plans minimize row/column conversions."

## Arrow Integration (Where It Fits)
Apache Arrow is primarily used for efficient JVM <-> Python data transfer (for example Pandas UDF paths), not as the default internal engine for all Spark SQL operators.

Practical takeaway:
- Arrow can reduce serialization overhead at language boundaries.
- Native Spark SQL expressions still outperform many Python UDF workflows.

## Performance Levers

### Query and model design
- Project only needed columns (column pruning).
- Push filters early (reduce decoded data).
- Prefer built-in SQL functions over Python UDFs.

### Data layout
- Columnar file formats: Parquet/ORC.
- Reasonable file sizes (avoid extreme small-files issue).
- Partition on common filter columns for pruning.

### Config knobs (context-dependent)
- `spark.sql.parquet.enableVectorizedReader` (generally keep enabled)
- `spark.sql.inMemoryColumnarStorage.compressed`
- `spark.sql.inMemoryColumnarStorage.batchSize`

Note: tune configs after fixing plan shape (projection/filter/join strategy/skew).

## Debugging Checklist
1. Inspect physical plan (`explain("formatted")`).
2. Identify conversion operators (`ColumnarToRow`, `RowToColumnar`).
3. Confirm file scan is vectorized for Parquet/ORC path.
4. Check Spark UI for stage time, scan metrics, spill, and skew.
5. Replace costly UDF paths with built-in expressions where possible.

## Common Pitfalls
- Assuming columnar path is always active end-to-end.
- Heavy Python UDF usage breaking vectorized flow.
- Ignoring conversion overhead between row and columnar segments.
- Over-tuning configs before verifying physical plan.

## Why It Matters
Understanding the columnar engine helps you:
- explain why Spark SQL is fast on Parquet/ORC workloads
- diagnose unexpected slowdowns from row/column conversions
- choose query patterns that preserve vectorized execution

## Related
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Performance-Tuning-Guide.md]]
- [[04-Data Engineering Library/Spark Deep Internals/WholeStageCodegen-Internals.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Tungsten-Memory-Management.md]]
