# Context (Token-Optimized)

## Purpose
This folder contains practical Snowflake engineering notes. Content depth is medium: implementation-oriented, not exhaustive theory.

## Canonical entrypoint
- `INDEX.md` is the navigation source of truth.

## Fast topic map
- Foundations: `01`, `02`, `03`
- Storage/pruning/perf: `04`, `05`, `12`
- Governance/security: `06`
- Pipelines: `07`, `08`
- Collaboration/sharing: `09`
- Ops + FinOps: `10`
- Interview prep: `11`

## Token-saving operating rules for Codex
1. Read `INDEX.md` + only the specific target file(s) for the user request.
2. Do not load all notes unless user asks for full rewrite.
3. For interview requests, default to `11` and pull supporting snippets from `04`, `05`, `10`, `12` only if needed.
4. For performance/cost questions, default to `04`, `05`, `10`, `12`.
5. Preserve current naming/numbering scheme when adding files.

## Writing style contract
- Medium-depth, practical, scenario-aware.
- Concise sections, clear checklists, real-world tradeoffs.
- Avoid overlong theory dumps.

## Known state
- No code/tests in this directory; Markdown knowledge base only.
- No pending broken links known at handover time.
