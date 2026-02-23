# Snowflake Interview Question

## Question
How did you optimize credit usage at your organization?

## Sample Answer
I treated credit optimization as a workload-management problem and focused on the biggest cost drivers first.

- Right-sized warehouses by workload: small ETL jobs ran on `X-SMALL`/`SMALL`, while heavy transforms used dedicated larger warehouses only when needed.
- Used shared warehouses for development workloads to avoid spinning up separate compute per developer/task.
- Enabled `AUTO_SUSPEND` (short idle windows) and `AUTO_RESUME` to eliminate idle burn.
- Separated BI, ETL, and ad hoc workloads into different warehouses so one noisy workload did not force all compute to scale up.
- Created separate warehouses per team in QA and production, so usage was attributable and each team was accountable for its credit consumption.
- Used multi-cluster only for concurrency-heavy BI windows instead of leaving it on all day.
- Optimized expensive queries: pruned unnecessary columns, filtered earlier, reduced large shuffles, and improved join patterns.
- Clustered large, high-scan tables on frequently filtered columns to improve pruning and reduce compute for repeated queries.
- Reduced full refresh patterns by using incremental loads and tasks/streams where possible.
- Added usage monitoring with account usage views and resource monitors, then set alerts and hard caps for non-production environments.
- Reviewed team-level usage regularly and partnered with teams to tune expensive queries, which improved both credits and runtime.
- Scheduled heavy jobs in controlled windows and prevented overlapping pipelines when concurrency was not required.

Result: we reduced monthly Snowflake credits while improving runtime consistency and dashboard performance.

## Follow-up Metrics to Mention
- Credit reduction percentage
- Runtime improvement percentage
- Warehouse idle-time reduction
- Cost per pipeline or dashboard

## More Snowflake Interview Q&A

## How is Snowflake different from traditional data warehouses?
Snowflake separates storage and compute, so you can scale warehouses independently without rebalancing data. It also supports near-zero-copy cloning, secure sharing, and semi-structured data (`VARIANT`) natively.

## When would you use clustering keys?
Use clustering keys for very large tables with frequent selective filters where micro-partition pruning is poor. I validate benefit using pruning/query profile first, because clustering has maintenance cost.

## What is Time Travel and how have you used it?
Time Travel lets you query or restore historical table states within retention limits. I use it for accidental delete recovery and point-in-time validation during pipeline incidents.

## What are Streams and Tasks in Snowflake?
Streams track table changes (CDC metadata), and Tasks schedule SQL execution. Together, they enable incremental ELT pipelines without full refreshes.

## How do you handle slowly changing dimensions in Snowflake?
For SCD Type 2, I use `MERGE` with effective start/end timestamps and current-row flags. I ensure idempotency and surrogate keys so reruns do not create duplicate history.

## How do you optimize slow Snowflake queries?
Start with Query Profile to find scan-heavy steps, bad joins, or spill. Then reduce scanned data (better filters/column pruning), tune join strategy, and resize warehouse only if SQL optimization is insufficient.

## What is the difference between `TRANSIENT` and permanent tables?
`TRANSIENT` tables have lower data protection (no Fail-safe), which reduces storage cost. I use them for staging/intermediate data, not for business-critical persisted datasets.

## How do you secure sensitive data in Snowflake?
Use RBAC with least privilege, masking/row access policies for PII, and separate roles for admin vs usage. I also enforce network policies and audit access via account usage views.

## How do you load files efficiently into Snowflake?
I use external/internal stages plus `COPY INTO` with file formats and load metadata checks. For large volume, I batch files at good size, use parallel loads, and avoid tiny-file patterns.

## What is zero-copy cloning and when is it useful?
Zero-copy cloning creates instant environment copies without duplicating physical storage initially. It is useful for safe QA testing, backfill validation, and fast rollback strategies.
