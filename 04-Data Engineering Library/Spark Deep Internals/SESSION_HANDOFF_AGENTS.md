# Session Handoff Agents (Token-Saving)

Purpose: carry work across sessions with minimal token usage.

## Global Rules (apply to all agents)
- Do not scan the full repository.
- Start with this order only:
  1. `SESSION_CONTEXT.md`
  2. User's latest prompt
  3. Only files explicitly listed in "Relevant Files" in `SESSION_CONTEXT.md`
- Use targeted search only (for example: `rg "pattern" Spark-Performance-Tuning-Guide.md Columnar-Execution-Engine.md`).
- Never run broad discovery commands like `rg --files`, recursive `find`, or full-tree indexing unless the user explicitly asks.
- If missing context blocks progress, ask one focused question instead of expanding scope.

## Agent: `handoff-coordinator`
- Goal: summarize current task and route execution.
- Inputs: `SESSION_CONTEXT.md`, latest user message.
- Output:
  - 3-6 line status summary
  - next concrete action
  - any blocker/question (single, specific)

## Agent: `sql-editor`
- Scope: `spark_pipeline.sql` only unless user asks otherwise.
- Workflow:
  1. Read only relevant SQL section(s).
  2. Make minimal patch.
  3. Return changed blocks + why.

## Agent: `python-editor`
- Scope: `spark_pipeline.py` only unless user asks otherwise.
- Workflow:
  1. Read only relevant function(s).
  2. Make minimal patch.
  3. Return changed blocks + why.

## Agent: `doc-updater`
- Scope: update only docs named in `SESSION_CONTEXT.md`.
- Avoid broad cross-link passes.
- Default priority docs in this workspace:
  1. `Spark-Performance-Tuning-Guide.md`
  2. `SparkSQL-Operations-Mapping-Cheatsheet.md`
  3. `Spark-Data-Modeling-Partitioning-and-Schema-Evolution.md`
  4. `Columnar-Execution-Engine.md`

## Session End Checklist
- Update `SESSION_CONTEXT.md`:
  - `Current Task`
  - `Last Completed`
  - `Next Step`
  - `Relevant Files`
  - `Open Questions`
- If a new file was created, add it to `Relevant Files` immediately.
