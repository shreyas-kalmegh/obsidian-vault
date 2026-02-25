# SQL Formatting Template (Interview Readability)

## Why This Format Works
- Keeps query intent obvious under time pressure.
- Reduces bugs in joins and filters.
- Makes complex multi-step logic easy to explain.

---

## Core Formatting Rules

1. Use uppercase SQL keywords (`SELECT`, `FROM`, `WHERE`, ...).
2. One selected column/expression per line.
3. Always alias tables in joins (`u`, `o`, etc.) and use qualified columns.
4. Put each join on a new line; put `ON` condition on next indented line.
5. Keep `WHERE` predicates one per line for fast debugging.
6. Prefer trailing comma style in `SELECT` and CTE column lists.
7. Add short section comments for each logical step in multi-CTE queries.
8. Keep consistent alias naming (`base`, `filtered`, `ranked`, `final`).

---

## 1) Single-Query Template

```sql
SELECT
    t.col1,
    t.col2,
    COUNT(*) AS cnt
FROM schema_name.table_name AS t
WHERE 1 = 1
    AND t.is_active = TRUE
    AND t.created_at >= DATE '2026-01-01'
GROUP BY
    t.col1,
    t.col2
HAVING COUNT(*) >= 5
ORDER BY
    cnt DESC,
    t.col1 ASC
LIMIT 100;
```

Notes:
- `WHERE 1 = 1` is optional; useful when iteratively adding filters.
- Use explicit `ASC`/`DESC` in interviews.

---

## 2) Join Query Template

```sql
SELECT
    u.user_id,
    u.email,
    o.order_id,
    o.total_amount
FROM users AS u
INNER JOIN orders AS o
    ON o.user_id = u.user_id
LEFT JOIN payments AS p
    ON p.order_id = o.order_id
WHERE 1 = 1
    AND u.country = 'US'
    AND o.created_at >= DATE '2026-01-01'
    AND p.status IS DISTINCT FROM 'failed'
ORDER BY
    o.created_at DESC,
    o.order_id DESC;
```

Gotcha:
- Don’t place right-table filters in `WHERE` if you need true left join behavior; keep them in `ON` when appropriate.

---

## 3) Window Function Template (Top-N / Latest Row)

```sql
WITH ranked AS (
    SELECT
        e.user_id,
        e.event_time,
        e.metric,
        ROW_NUMBER() OVER (
            PARTITION BY e.user_id
            ORDER BY e.event_time DESC, e.event_id DESC
        ) AS rn
    FROM events AS e
)
SELECT
    r.user_id,
    r.event_time,
    r.metric
FROM ranked AS r
WHERE r.rn = 1;
```

Notes:
- Always include deterministic tie-breakers in window `ORDER BY`.

---

## 4) Multi-Step CTE Template (Complex Interview Query)

```sql
WITH
-- 1) Base extraction
base AS (
    SELECT
        o.order_id,
        o.user_id,
        o.created_at,
        o.amount,
        o.status
    FROM orders AS o
    WHERE o.created_at >= DATE '2026-01-01'
),

-- 2) Apply business filters
filtered AS (
    SELECT
        b.order_id,
        b.user_id,
        b.created_at,
        b.amount
    FROM base AS b
    WHERE b.status = 'completed'
      AND b.amount > 0
),

-- 3) Derive per-user aggregates
user_agg AS (
    SELECT
        f.user_id,
        COUNT(*) AS order_cnt,
        SUM(f.amount) AS total_amount,
        MAX(f.created_at) AS latest_order_at
    FROM filtered AS f
    GROUP BY
        f.user_id
),

-- 4) Final ranking/output shaping
final_ranked AS (
    SELECT
        ua.user_id,
        ua.order_cnt,
        ua.total_amount,
        ua.latest_order_at,
        DENSE_RANK() OVER (
            ORDER BY ua.total_amount DESC, ua.user_id ASC
        ) AS spend_rank
    FROM user_agg AS ua
)
SELECT
    fr.user_id,
    fr.order_cnt,
    fr.total_amount,
    fr.latest_order_at,
    fr.spend_rank
FROM final_ranked AS fr
WHERE fr.spend_rank <= 10
ORDER BY
    fr.spend_rank ASC,
    fr.user_id ASC;
```

Why this is interview-friendly:
- Each CTE has one job.
- Easy to test each step by selecting from intermediate CTEs.
- Easy to explain tradeoffs and correctness.

---

## 5) Update/Delete with Safety Template

```sql
-- Preview impacted rows first
SELECT
    t.id,
    t.status
FROM target_table AS t
WHERE t.status = 'stale';

-- Then write inside transaction
BEGIN;

UPDATE target_table AS t
SET status = 'archived'
WHERE t.status = 'stale'
RETURNING t.id, t.status;

-- COMMIT;
ROLLBACK;
```

Notes:
- In interviews, mention “preview first, then write.”
- Show `RETURNING` to validate exactly what changed.

---

## 6) Naming Convention Cheatsheet

- Tables:
  - `u` = users
  - `o` = orders
  - `p` = payments
- CTEs:
  - `base`, `filtered`, `agg`, `ranked`, `final`
- Computed columns:
  - suffixes like `_cnt`, `_amt`, `_at`, `_flag`, `_rank`

Consistency beats cleverness.

---

## 7) Pre-Submission Checklist (Interview)

- Deterministic ordering (`ORDER BY ... , id`).
- Correct `NULL` handling (`IS NULL`, `COALESCE`, `IS DISTINCT FROM`).
- Join cardinality understood (no accidental duplication).
- `LEFT JOIN` semantics preserved (filter placement checked).
- Edge cases covered (empty set, ties, duplicates).
- Query readable enough to explain in 60 seconds.
