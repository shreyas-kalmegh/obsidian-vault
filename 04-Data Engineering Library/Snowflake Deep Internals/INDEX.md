# Snowflake Deep Internals - Index

This set of notes is written for practical engineering work: enough depth to reason about tradeoffs, design decisions, and operational behavior, without becoming a full textbook.

## Suggested reading order
1. `01-Architecture-Foundations.md`
2. `02-Storage-Compute-Cloud-Services.md`
3. `03-Virtual-Warehouses-and-Concurrency.md`
4. `04-Micro-Partitions-Clustering-Pruning.md`
5. `05-Query-Performance-Tuning.md`
6. `06-Security-Governance-and-Access-Control.md`
7. `07-Data-Ingestion-Patterns.md`
8. `08-Transformations-Tasks-and-Streams.md`
9. `09-Data-Sharing-and-Collaboration.md`
10. `10-Operations-Cost-and-Reliability.md`
11. `11-Interview-Scenario-Prep.md`
12. `12-Data-Skew-in-Micro-Partitions.md`

## Codex session files
- `CONTEXT.md` (token-optimized working context)
- `SESSION_HANDOVER.md` (what was done, what remains)

## How to use these notes
- Start with architecture and storage/compute separation if you are new to Snowflake.
- Jump to performance and micro-partition notes when debugging slow queries.
- Use ingestion + transformations together when building production ELT.
- Keep the operations/cost note open while designing pipelines to avoid expensive defaults.
- Use interview prep note for scenario-style practice and answer structuring.
- Use the short skew note as a quick diagnostic checklist.

## Scope
These notes focus on common real-world workloads:
- Analytics and BI
- Batch and micro-batch ELT
- Data sharing across teams/organizations
- Governance in multi-team environments
