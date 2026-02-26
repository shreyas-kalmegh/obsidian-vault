# Session Context

## Project
Spark Deep Internals knowledge base with SQL/Python pipeline examples.

## Current Task
Keep docs interview-focused and token-efficient, with emphasis on Spark SQL-first prep and performance internals.

## Last Completed
- Added SQL-first interview mapping sheet:
  - `SparkSQL-Operations-Mapping-Cheatsheet.md`
  - Includes multi-step SQL example with `REPARTITION`, `COALESCE`, and `INSERT INTO`.
- Added data modeling guide:
  - `Spark-Data-Modeling-Partitioning-and-Schema-Evolution.md`
  - Covers partition strategy + schema evolution examples.
- Updated `Spark-Performance-Tuning-Guide.md` with:
  - CDC schema evolution behavior at file level
  - `NOT NULL` added-column caveat (full rewrite-like effect only with emitted backfill updates or explicit migration).
- Expanded `Columnar-Execution-Engine.md` from template to practical deep-dive.

## Next Step
For new requests, update only the specifically asked note/file, then reflect outcomes in this context file.

## Relevant Files
- `SESSION_HANDOFF_AGENTS.md`
- `SESSION_CONTEXT.md`
- `SparkSQL-Operations-Mapping-Cheatsheet.md`
- `Spark-Data-Modeling-Partitioning-and-Schema-Evolution.md`
- `Spark-Performance-Tuning-Guide.md`
- `Columnar-Execution-Engine.md`
- `spark_pipeline.sql`
- `spark_pipeline.py`

## Open Questions
- Should CDC behavior get its own dedicated note (separate from performance guide)?
- Should we add a compact Spark SQL interview Q&A note (one-page rapid revision)?

## Fast Start (for next session)
1. Read `SESSION_CONTEXT.md`.
2. Read `SESSION_HANDOFF_AGENTS.md`.
3. Open only the directly relevant file(s) from `Relevant Files`.
4. Avoid repo-wide discovery unless user explicitly asks.
