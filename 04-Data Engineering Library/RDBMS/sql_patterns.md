# SQL Interview Patterns: Identification + Templates

## How to Identify Patterns Quickly

Ask these first:
1. Do I need one row per entity, per group, or global aggregate?
2. Is this matching records, missing records, or comparing snapshots?
3. Is there "latest", "top N", or "running" in wording? (window function signal)
4. Is pagination required at scale? (keyset pagination signal)
5. Is this data quality (duplicates, anomalies, missing dimension rows)?
6. Do I need write-safe logic (`upsert`, dedup delete, transaction)?

---

## Quick Mapping (Signal -> Pattern)

| Problem Signal | Use This Pattern |
|---|---|
| "latest per user" | `ROW_NUMBER() ... WHERE rn = 1` |
| "top N per category" | partitioned ranking |
| "customers without orders" | anti-join (`LEFT ... IS NULL` / `NOT EXISTS`) |
| "remove duplicates" | rank rows + delete where `rn > 1` |
| "running total" | window aggregate with `ORDER BY` |
| "compare with previous row" | `LAG` / `LEAD` |
| "report with subtotals" | `ROLLUP`/`CUBE`/`GROUPING SETS` |
| "upsert" | `INSERT ... ON CONFLICT DO UPDATE` |
| "page 1000 is slow" | keyset pagination |
| "hierarchy/tree" | recursive CTE |

---

## 1) Latest Row Per Entity

When asked:
- "current status per user"
- "most recent order per customer"

```sql
WITH ranked AS (
    SELECT
        t.*,
        ROW_NUMBER() OVER (
            PARTITION BY t.user_id
            ORDER BY t.event_time DESC, t.event_id DESC
        ) AS rn
    FROM events AS t
)
SELECT *
FROM ranked
WHERE rn = 1;
```

Caveat:
- Add deterministic tie-breaker (`event_id DESC`).

---

## 2) Top N Per Group

When asked:
- "top 3 products per category"

```sql
WITH ranked AS (
    SELECT
        p.category_id,
        p.product_id,
        p.revenue,
        ROW_NUMBER() OVER (
            PARTITION BY p.category_id
            ORDER BY p.revenue DESC, p.product_id ASC
        ) AS rn
    FROM product_sales AS p
)
SELECT *
FROM ranked
WHERE rn <= 3;
```

Use:
- `ROW_NUMBER` => strict N rows
- `RANK` / `DENSE_RANK` => include ties semantics

---

## 3) Anti-Join (Find Missing Records)

When asked:
- "customers with no orders"
- "dimension keys not present in fact"

```sql
SELECT c.*
FROM customers AS c
LEFT JOIN orders AS o
    ON o.customer_id = c.customer_id
WHERE o.customer_id IS NULL;
```

Alternative:
```sql
SELECT c.*
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
);
```

Caveat:
- Avoid `NOT IN` when subquery may contain `NULL`.

---

## 4) Semi-Join (Keep Rows That Have Match)

When asked:
- "users who purchased at least once"

```sql
SELECT u.*
FROM users u
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.user_id
);
```

Why:
- Avoids duplicate multiplication from joins when only existence is needed.

---

## 5) Duplicate Detection

When asked:
- "find duplicate emails"

```sql
SELECT email, COUNT(*) AS cnt
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

---

## 6) Deduplicate While Keeping Best Row

When asked:
- "delete duplicates, keep newest"

```sql
WITH d AS (
    SELECT
        id,
        ROW_NUMBER() OVER (
            PARTITION BY business_key
            ORDER BY updated_at DESC, id DESC
        ) AS rn
    FROM t
)
DELETE FROM t
USING d
WHERE t.id = d.id
  AND d.rn > 1;
```

Caveat:
- Test with a `SELECT` version first.

---

## 7) Running Total / Moving Window

When asked:
- "cumulative revenue"
- "7-day rolling avg"

```sql
SELECT
    user_id,
    dt,
    amount,
    SUM(amount) OVER (
        PARTITION BY user_id
        ORDER BY dt
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_amount
FROM payments;
```

Rolling avg example:
```sql
AVG(amount) OVER (
    PARTITION BY user_id
    ORDER BY dt
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
) AS avg_7d
```

---

## 8) Compare Current vs Previous (LAG/LEAD)

When asked:
- "day-over-day change"
- "detect state transitions"

```sql
SELECT
    dt,
    value,
    value - LAG(value) OVER (ORDER BY dt) AS delta
FROM metrics;
```

---

## 9) Gaps and Islands (Consecutive Sequences)

When asked:
- "longest consecutive login streak"

Core idea:
- Build grouping key via `date - row_number()` or similar arithmetic.

```sql
WITH x AS (
    SELECT
        user_id,
        login_date,
        login_date - (ROW_NUMBER() OVER (
            PARTITION BY user_id
            ORDER BY login_date
        ))::int AS grp
    FROM logins
)
SELECT
    user_id,
    MIN(login_date) AS streak_start,
    MAX(login_date) AS streak_end,
    COUNT(*) AS streak_len
FROM x
GROUP BY user_id, grp;
```

---

## 10) Pivot / Conditional Aggregation

When asked:
- "show success vs failure metrics in columns"

```sql
SELECT
    user_id,
    SUM(amount) FILTER (WHERE status = 'success') AS success_amount,
    SUM(amount) FILTER (WHERE status = 'failed')  AS failed_amount
FROM txns
GROUP BY user_id;
```

---

## 11) Keyset Pagination (Scalable)

When asked:
- "offset is slow on deep pages"

```sql
SELECT id, created_at, payload
FROM events
WHERE (created_at, id) < ($last_created_at, $last_id)
ORDER BY created_at DESC, id DESC
LIMIT 50;
```

Caveat:
- Requires stable deterministic ordering + matching index.

---

## 12) Upsert Pattern

When asked:
- "insert if new else update"

```sql
INSERT INTO users (user_id, email, updated_at)
VALUES ($1, $2, NOW())
ON CONFLICT (user_id)
DO UPDATE SET
    email = EXCLUDED.email,
    updated_at = EXCLUDED.updated_at;
```

---

## 13) SCD Type 2 (Interview Variant)

When asked:
- "track historical changes"

Pattern steps:
1. End-date existing current row
2. Insert new current row
3. Keep `is_current`/validity ranges

```sql
BEGIN;

UPDATE dim_customer
SET valid_to = NOW(), is_current = FALSE
WHERE customer_id = $1
  AND is_current = TRUE
  AND email IS DISTINCT FROM $2;

INSERT INTO dim_customer (customer_id, email, valid_from, valid_to, is_current)
SELECT $1, $2, NOW(), NULL, TRUE
WHERE NOT EXISTS (
    SELECT 1
    FROM dim_customer
    WHERE customer_id = $1
      AND is_current = TRUE
      AND email = $2
);

COMMIT;
```

---

## 14) Recursive Hierarchy Query

When asked:
- "org tree"
- "all descendants of manager"

```sql
WITH RECURSIVE org AS (
    SELECT id, manager_id, 1 AS lvl
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.manager_id, o.lvl + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT * FROM org;
```

Caveat:
- Add depth cap or cycle protection in real systems.

---

## 15) Cohort/Retention Pattern

When asked:
- "monthly retention"

Template idea:
1. Derive cohort month (first activity)
2. Join future activity by month offset
3. Aggregate retained users by cohort x month_number

```sql
WITH first_seen AS (
    SELECT user_id, DATE_TRUNC('month', MIN(event_time)) AS cohort_month
    FROM events
    GROUP BY user_id
),
activity AS (
    SELECT
        e.user_id,
        DATE_TRUNC('month', e.event_time) AS activity_month
    FROM events e
    GROUP BY e.user_id, DATE_TRUNC('month', e.event_time)
)
SELECT
    f.cohort_month,
    EXTRACT(YEAR FROM age(a.activity_month, f.cohort_month)) * 12
      + EXTRACT(MONTH FROM age(a.activity_month, f.cohort_month)) AS month_number,
    COUNT(DISTINCT a.user_id) AS retained_users
FROM first_seen f
JOIN activity a ON a.user_id = f.user_id
GROUP BY f.cohort_month, month_number
ORDER BY f.cohort_month, month_number;
```

---

## 16) Slowly Changing Fact Comparison (Snapshot Diff)

When asked:
- "find added/removed/changed rows between snapshots"

```sql
SELECT
    COALESCE(a.id, b.id) AS id,
    CASE
        WHEN a.id IS NULL THEN 'added'
        WHEN b.id IS NULL THEN 'removed'
        WHEN a.hash_val IS DISTINCT FROM b.hash_val THEN 'changed'
        ELSE 'same'
    END AS diff_type
FROM snapshot_old b
FULL OUTER JOIN snapshot_new a
    ON a.id = b.id;
```

---

## 17) Performance Pattern Checklist

Before finalizing query:
- Are filters pushed early (`WHERE` before `GROUP BY`)?
- Are join keys indexed?
- Is `SELECT *` avoidable?
- Are you multiplying rows accidentally by many-to-many joins?
- Could `EXISTS` replace join for existence checks?
- Do you need keyset over offset pagination?
- Did you verify plan with `EXPLAIN (ANALYZE, BUFFERS)`?

---

## 18) High-Value Gotchas and Caveats

- `COUNT(col)` ignores `NULL`; `COUNT(*)` does not.
- `LEFT JOIN` can become inner join if right-table filters are put in `WHERE`.
- Missing tie-breakers produce nondeterministic top-1/top-N.
- `NOT IN` with `NULL` behaves unexpectedly.
- Window functions run after `WHERE` but before final `ORDER BY` output semantics.
- Overusing CTEs can hurt readability/performance if every step is trivial.
- Always validate timezone/date truncation assumptions in time-based questions.

---

## 19) Interview Answer Structure (60-Second Flow)

1. State the pattern: "This is latest-per-group -> window + row_number."
2. Explain correctness: partition key + ordering + tie-breaker.
3. Mention edge cases: `NULL`, duplicates, ties.
4. Mention performance: useful index and expected scan/join behavior.
5. Provide clean SQL and expected output shape.
