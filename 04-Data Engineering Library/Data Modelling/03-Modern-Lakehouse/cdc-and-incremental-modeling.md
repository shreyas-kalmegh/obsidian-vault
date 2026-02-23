# CDC and Incremental Modeling

## Core Concepts
- Capture inserts, updates, deletes from source logs.
- Apply idempotent upserts/merges downstream.
- Preserve ordering and watermarks where required.

## Design Patterns
- High watermark on event timestamp
- Merge by business key + effective timestamp
- Soft delete propagation strategy

## Checklist
- [ ] Exactly-once or idempotent semantics defined
- [ ] Late and out-of-order handling documented
- [ ] Delete semantics (hard/soft) explicit

## Common Mistakes
- Using load timestamp as event truth
- Missing reprocessing strategy for historical corrections

## Interview Prompts
- How do you recover from a bad CDC deployment?

## Related Notes
- [[late-arriving-data]]
- [[scd-types]]
