# Snowflake Interview Prep - Scenario-Based Questions

This note is optimized for data engineering interviews where the interviewer tests practical decision-making instead of pure definitions.

## How to answer scenario questions
Use a repeatable structure:
1. Clarify workload and constraints (latency, SLA, cost target, concurrency).
2. Diagnose with Snowflake telemetry (query history, warehouse usage, bytes scanned, queue time).
3. Propose phased fixes (quick wins, medium-term design, guardrails).
4. Define measurable outcomes (credits/day, p95 latency, failure rate).

## Scenario 1: Credit usage is growing fast
### Prompt
"Our Snowflake bill increased 40% in two months. Dashboards are also slower during business hours. How would you optimize credit usage without hurting reliability?"

### Strong answer outline
1. Baseline the cost drivers:
- Break down credits by warehouse, time window, and workload class (BI vs ELT vs ad hoc).
- Identify idle runtime, queueing, and top expensive queries.

2. Separate cost vs performance causes:
- High queue time -> concurrency/isolation problem.
- High execution time and scan bytes -> SQL/modeling/pruning problem.

3. Quick wins (first 1-2 weeks):
- Reduce auto-suspend on low-duty-cycle warehouses.
- Split BI and ETL into dedicated warehouses.
- Right-size oversized warehouses used for light ad hoc traffic.
- Cancel/limit runaway queries and add role-based limits.

4. Medium-term fixes:
- Tune high-scan queries (predicate rewrite, selective projections, pre-aggregation).
- Improve micro-partition pruning; evaluate clustering only for large hot tables.
- Materialize repeatedly expensive transformations where refresh economics make sense.

5. Governance guardrails:
- Resource monitors with threshold alerts and action policies.
- Warehouse naming/tagging per team for cost ownership.
- Weekly FinOps review: top N queries and idle burn.

6. Success metrics:
- 20-30% credit reduction in 4-8 weeks.
- p95 dashboard latency stable or improved.
- Fewer queue spikes during ETL windows.

### Red flags to avoid in interview answers
- "Just downsize all warehouses" (breaks SLAs).
- "Use one big warehouse for everything" (contention and no ownership).
- No measurement plan before and after changes.

## Scenario 2: Dashboard latency spikes at 9 AM
### Prompt
"Executives complain dashboards are slow every morning between 9-10 AM."

### Strong answer outline
- Confirm if slowdown is queueing or query complexity.
- Check concurrent query surge and warehouse queue time.
- Move ETL jobs off BI warehouse if shared.
- Consider multi-cluster for bursty BI concurrency.
- Precompute heavy dashboard models before business hours.
- Track p95 latency and queue duration after changes.

## Scenario 3: Incremental pipeline misses updates
### Prompt
"A daily incremental pipeline is fast but occasionally misses changed records."

### Strong answer outline
- Validate watermark logic and late-arriving data assumptions.
- Use deterministic merge keys and idempotent `MERGE` semantics.
- Add replay window (for example, reprocess last N days) to capture late updates.
- Use streams/tasks carefully with observability on lag and failed runs.
- Add reconciliation checks (source vs target counts, hash totals).

## Scenario 4: Secure PII while enabling analyst access
### Prompt
"Analysts need customer behavior data, but compliance requires strict PII protection."

### Strong answer outline
- Implement RBAC with least privilege roles.
- Expose curated views/marts, not raw PII tables.
- Apply dynamic masking and row access policies.
- Tag/classify sensitive columns and audit role usage.
- Keep grant and policy definitions in version-controlled SQL.

## Scenario 5: Many teams query same core tables
### Prompt
"Data platform has noisy-neighbor issues because all teams run on shared compute."

### Strong answer outline
- Isolate workloads by warehouse per team/function.
- Define SLO tiers (interactive BI, scheduled ELT, experimentation).
- Enforce cost accountability through warehouse tags and monitors.
- Publish shared semantic marts to reduce duplicated heavy transformations.

## Rapid-fire interviewer follow-ups
### "When would you scale up vs scale out?"
- Scale up (bigger warehouse): single heavy query runtime bottleneck.
- Scale out (multi-cluster): many concurrent queries causing queueing.

### "How do you prove optimization worked?"
- Compare before/after for credits, queue time, execution time, scanned bytes, and p95 dashboard latency.

### "What is your first SQL optimization check?"
- Predicate selectivity and scanned bytes vs rows returned.

## 30-60-90 day plan (if asked for ownership mindset)
### 30 days
- Build visibility dashboards for warehouse credits, queue time, and top expensive queries.
- Implement quick wins on suspend settings and workload isolation.

### 60 days
- Tune top cost/perf offenders; improve model layer for reuse.
- Add resource monitors and query governance policies.

### 90 days
- Standardize platform playbooks (sizing, incident response, backfill strategy).
- Institutionalize monthly Snowflake cost/performance review with domain teams.
