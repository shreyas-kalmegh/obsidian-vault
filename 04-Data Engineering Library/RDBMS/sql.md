# SQL Interview Cheatsheet (PostgreSQL-Oriented)

## Quick Reference Table

| Topic | What Interviewers Check | High-Value Keywords |
|---|---|---|
| Joins | Can you choose correct join semantics | `INNER`, `LEFT`, `EXISTS`, anti-join |
| Aggregation | Can you summarize correctly | `GROUP BY`, `HAVING`, `ROLLUP`, `CUBE` |
| Window functions | Can you solve ranking/running queries | `ROW_NUMBER`, `RANK`, `LAG`, `LEAD` |
| Data modeling | Do you understand integrity/anomalies | keys, FKs, normal forms |
| Transactions | Can you reason about correctness | ACID, `BEGIN/COMMIT/ROLLBACK` |
| Indexing | Can you reason about performance tradeoffs | B-tree, partial/index-only, `EXPLAIN` |
| Upsert/pipelines | Can you handle real write paths | `ON CONFLICT`, CTEs, `RETURNING` |

---

## 1) SQL Execution Order (Mental Model)

Logical order (simplified):
1. `FROM` / `JOIN`
2. `WHERE`
3. `GROUP BY`
4. `HAVING`
5. `SELECT`
6. `ORDER BY`
7. `LIMIT/OFFSET`

Why this matters:
- You cannot use aggregate aliases in `WHERE`.
- Filter early in `WHERE` before grouping when possible.

---

## 2) NULL Handling

```sql
SELECT COALESCE(discount, 0) AS discount_value
FROM prices;
```

Patterns:
- `COALESCE(a, b, c)` for fallback values.
- `CASE` for conditional replacement.

Gotchas:
- `NULL = NULL` is not true; use `IS NULL`.
- `NOT IN (...)` with `NULL` in the subquery can return no rows unexpectedly.

---

## 3) Arithmetic, Data Types, and NULLs

### Integer vs decimal math
- If both operands are integer types, many engines perform integer division.
- Cast one side to decimal/numeric to preserve fractions.

```sql
-- integer division (can truncate)
SELECT 5 / 2;  -- often 2

-- decimal division
SELECT 5::numeric / 2;  -- 2.5
```

### Aggregate arithmetic
- `SUM(int_col)` can stay integer-like; cast before division when needed.
- Use `NULLIF(denominator, 0)` to avoid divide-by-zero.

```sql
SELECT
    ROUND(
        SUM(price::numeric * units) / NULLIF(SUM(units), 0),
        2
    ) AS avg_price
FROM sales;
```

### `NULL` behavior in arithmetic
- Any arithmetic with `NULL` returns `NULL`.
- Aggregates:
  - `COUNT(col)` ignores `NULL`
  - `COUNT(*)` counts rows
  - `SUM/AVG/MIN/MAX` ignore `NULL` inputs

```sql
SELECT
    10 + NULL AS a,                -- NULL
    COALESCE(10 + NULL, 0) AS b;   -- 0
```

### Output formatting caveat
- `ROUND(x, 2)` rounds value but display may still show `2` instead of `2.00`.
- Cast to fixed-scale numeric for consistent formatting:

```sql
SELECT ROUND(2::numeric, 2)::numeric(10,2);  -- 2.00
```

Interview checklist:
- Explicitly cast before division.
- Protect denominator with `NULLIF`.
- Use `COALESCE` only where business-default value is valid.
- Mention integer-vs-decimal behavior and `NULL` propagation.

---

## 4) Joins You Must Know

### Inner Join
```sql
SELECT a.id, b.value
FROM a
JOIN b ON b.id = a.id;
```

### Left Join (preserve left side)
```sql
SELECT a.*, b.value
FROM a
LEFT JOIN b ON b.id = a.id;
```

### Semi Join (`EXISTS`)
```sql
SELECT a.*
FROM a
WHERE EXISTS (
  SELECT 1
  FROM b
  WHERE b.id = a.id
);
```

### Anti Join (find missing matches)
```sql
SELECT a.*
FROM a
LEFT JOIN b ON b.id = a.id
WHERE b.id IS NULL;
```

Caveat:
- Prefer `EXISTS`/anti-join over `IN`/`NOT IN` when `NULL` handling is ambiguous.

---

## 5) Aggregation Patterns

### Basic group + filter groups
```sql
SELECT department_id, COUNT(*) AS n
FROM employees
GROUP BY department_id
HAVING COUNT(*) >= 5;
```

### Grouping extensions
- `ROLLUP(c1, c2, c3)` -> hierarchical subtotals + grand total
- `CUBE(c1, c2, c3)` -> all subtotal combinations
- `GROUPING SETS (...)` -> custom subtotal combinations

```sql
SELECT c1, c2, SUM(val)
FROM t
GROUP BY GROUPING SETS ((c1, c2), (c1), ());
```

`GROUPING SETS` example (explicit custom subtotals):
```sql
SELECT
  region,
  product,
  SUM(revenue) AS revenue
FROM sales
GROUP BY GROUPING SETS (
  (region, product),  -- detail
  (region),           -- subtotal by region
  (product),          -- subtotal by product
  ()                  -- grand total
);
```

`CUBE` example (all combinations):
```sql
SELECT
  region,
  channel,
  SUM(revenue) AS revenue
FROM sales
GROUP BY CUBE (region, channel);
```

Use `GROUPING(...)` to identify subtotal rows:
```sql
SELECT
  region,
  channel,
  SUM(revenue) AS revenue,
  GROUPING(region)  AS g_region,
  GROUPING(channel) AS g_channel
FROM sales
GROUP BY CUBE (region, channel);
```

Gotcha:
- `WHERE` filters rows before grouping; `HAVING` filters groups after aggregation.

---

## 6) Window Functions (Very Common)

### Rank rows per group
```sql
SELECT
  user_id,
  event_time,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time DESC) AS rn
FROM events;
```

### Most recent row per user
```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time DESC) AS rn
  FROM events
)
SELECT *
FROM ranked
WHERE rn = 1;
```

### Running total
```sql
SELECT
  user_id,
  event_time,
  amount,
  SUM(amount) OVER (PARTITION BY user_id ORDER BY event_time) AS running_amount
FROM payments;
```

### Window frame bounds (`ROWS` / `RANGE`)
Common bounds:
- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` -> running aggregate
- `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` -> rolling 7 rows
- `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` -> centered window
- `RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW` -> value/time-based range (engine support varies)

Running sum with explicit frame:
```sql
SELECT
  user_id,
  event_time,
  amount,
  SUM(amount) OVER (
    PARTITION BY user_id
    ORDER BY event_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_amount
FROM payments;
```

Rolling 7-row average:
```sql
SELECT
  user_id,
  event_time,
  amount,
  AVG(amount) OVER (
    PARTITION BY user_id
    ORDER BY event_time
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS avg_last_7_rows
FROM payments;
```

Gotcha:
- With `ORDER BY`, default frame can behave like running aggregate; define frame explicitly.
- `ROWS` counts physical rows; `RANGE` groups peers with same `ORDER BY` value and can produce different results.

---

## 7) CTEs and Recursive Queries

### Standard CTE
```sql
WITH high_value AS (
  SELECT customer_id, SUM(total) AS spend
  FROM orders
  GROUP BY customer_id
)
SELECT *
FROM high_value
WHERE spend > 10000;
```

### Recursive CTE skeleton
```sql
WITH RECURSIVE hierarchy AS (
  SELECT id, manager_id, 1 AS lvl
  FROM employees
  WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.manager_id, h.lvl + 1
  FROM employees e
  JOIN hierarchy h ON e.manager_id = h.id
)
SELECT * FROM hierarchy;
```

Guideline:
- Use `UNION ALL` unless dedup is required.

---

## 8) DML Write Patterns

### Insert + returning
```sql
INSERT INTO users(name, email)
VALUES ('Ana', 'ana@x.com')
RETURNING id;
```

### Update from another table
```sql
UPDATE t1
SET c1 = t2.new_value
FROM t2
WHERE t1.key = t2.key;
```

### Delete using join key
```sql
DELETE FROM contacts c
USING blacklist b
WHERE c.phone = b.phone;
```

### Upsert (`ON CONFLICT`)
```sql
INSERT INTO customers(name, email)
VALUES ('Microsoft', 'hotline@microsoft.com')
ON CONFLICT (name)
DO UPDATE SET email = EXCLUDED.email;
```

Gotcha:
- Upsert target must match a unique constraint/index.

---

## 9) DDL, Keys, and Constraints

### Must-know constraints
- `PRIMARY KEY` (unique + not null)
- `FOREIGN KEY` (`ON DELETE CASCADE/SET NULL/...`)
- `UNIQUE`
- `CHECK`
- `NOT NULL`

```sql
CREATE TABLE orders (
  id BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL,
  amount NUMERIC CHECK (amount > 0),
  CONSTRAINT fk_customer
    FOREIGN KEY (customer_id)
    REFERENCES customers(id)
    ON DELETE CASCADE
);
```

Data anomaly reminders:
- Insert anomaly
- Update anomaly
- Delete anomaly

Normal forms:
- 1NF, 2NF, 3NF, BCNF (interview-level usually enough)

---

## 10) Indexing and Performance

### Index basics
- B-tree default: equality + range + prefix `LIKE 'foo%'`
- Hash: equality-only
- GIN: `jsonb`/arrays/full-text style multi-valued search
- BRIN: huge naturally ordered tables

### Useful index patterns
```sql
-- expression index
CREATE INDEX idx_lower_email ON users (LOWER(email));

-- partial index
CREATE INDEX idx_active_orders ON orders (customer_id)
WHERE status = 'active';

-- unique index
CREATE UNIQUE INDEX idx_users_email ON users (email);
```

Caveats:
- Every index improves reads but slows writes and uses storage.
- Indexes are only used when predicates align with indexed expression/order/selectivity.
- Leading wildcard (`LIKE '%abc'`) typically cannot use normal B-tree index efficiently.

---

## 11) Query Planning (`EXPLAIN`)

```sql
EXPLAIN ANALYZE
SELECT ...;
```

Look for:
- Seq scan vs index scan
- estimated rows vs actual rows mismatch
- join strategy (`Nested Loop`, `Hash Join`, `Merge Join`)

Safe pattern for testing writes:

```sql
BEGIN;
  EXPLAIN ANALYZE UPDATE ...;
ROLLBACK;
```

---

## 12) Transactions and Isolation Basics

```sql
BEGIN;
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
COMMIT;
```

ACID:
- Atomicity, Consistency, Isolation, Durability

Gotchas:
- Long transactions hold locks longer and increase contention.
- Missing transaction boundaries can leave multi-step writes inconsistent.

---

## 13) Pagination and Retrieval Patterns

### Offset pagination
```sql
SELECT id, created_at
FROM events
ORDER BY created_at DESC
OFFSET 100 LIMIT 20;
```

### Keyset pagination (preferred at scale)
```sql
SELECT id, created_at
FROM events
WHERE (created_at, id) < ('2026-01-01', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Gotcha:
- Always use deterministic `ORDER BY` for pagination.

---

## 14) SQL Interview Patterns (High Frequency)

- Latest row per entity: `ROW_NUMBER() ... WHERE rn = 1`
- Top N per group: `ROW_NUMBER()/RANK()` with partition
- Gaps and islands: window functions + date/id arithmetic
- Anti-join missing records: `LEFT JOIN ... WHERE right.id IS NULL`
- Dedup rows: CTE with `ROW_NUMBER` then keep `rn = 1`
- Running totals and moving averages: window frame functions
- Pivot-ish reporting: `SUM(...) FILTER (WHERE ...)`

---

## 15) PostgreSQL-Specific Handy Features

- `RETURNING` on `INSERT/UPDATE/DELETE`
- `ON CONFLICT` for upsert
- `LATERAL` joins for per-row dependent subqueries
- Materialized views + `REFRESH MATERIALIZED VIEW`
- `ILIKE` for case-insensitive matching

`LATERAL` example:
```sql
SELECT u.id, x.last_order_time
FROM users u
LEFT JOIN LATERAL (
  SELECT o.created_at AS last_order_time
  FROM orders o
  WHERE o.user_id = u.id
  ORDER BY o.created_at DESC
  LIMIT 1
) x ON true;
```

---

## 16) High-Value Gotchas and Caveats

- `NOT IN` + `NULL` trap; prefer `NOT EXISTS`.
- `COUNT(*)` counts rows; `COUNT(col)` ignores `NULL`.
- `LEFT JOIN` + `WHERE right.col = ...` can accidentally turn into inner join.
- Non-deterministic ordering without explicit `ORDER BY`.
- Selecting non-grouped columns with aggregation is invalid (or non-portable in some engines).
- Index not used due to function wrapping (`WHERE LOWER(col)=...` without expression index).
- Over-indexing can hurt write-heavy workloads.
- CTE materialization/inlining behavior differs by PostgreSQL version and query shape.

---

## 17) Final Interview Checklist

- Confirm business requirement and edge cases (`NULL`, duplicates, ties).
- Start with correct logic, then optimize.
- Explain join choice and expected row cardinality.
- Mention index strategy for critical predicates.
- Validate with sample output and corner cases.
- Discuss tradeoffs: readability, correctness, performance.

---

## 18) Common Interview Questions + Query Templates

1. Latest row per entity  
Template:
```sql
WITH ranked AS (
  SELECT t.*,
         ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY event_time DESC) AS rn
  FROM t
)
SELECT *
FROM ranked
WHERE rn = 1;
```

2. Top N per group  
Template:
```sql
WITH ranked AS (
  SELECT t.*,
         ROW_NUMBER() OVER (PARTITION BY group_id ORDER BY metric DESC) AS rn
  FROM t
)
SELECT *
FROM ranked
WHERE rn <= 3;
```

3. Find duplicates by key  
Template:
```sql
SELECT key_col, COUNT(*) AS cnt
FROM t
GROUP BY key_col
HAVING COUNT(*) > 1;
```

4. Remove duplicates but keep newest row  
Template:
```sql
WITH d AS (
  SELECT id,
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

5. Missing records (anti-join)  
Template:
```sql
SELECT a.*
FROM a
LEFT JOIN b ON b.id = a.id
WHERE b.id IS NULL;
```

6. Running total by user  
Template:
```sql
SELECT user_id, event_time, amount,
       SUM(amount) OVER (
         PARTITION BY user_id
         ORDER BY event_time
       ) AS running_sum
FROM payments;
```

7. Day-over-day change (`LAG`)  
Template:
```sql
SELECT dt,
       value,
       value - LAG(value) OVER (ORDER BY dt) AS delta
FROM metrics;
```

8. Upsert into dimension/reference table  
Template:
```sql
INSERT INTO dim_user(user_id, email, updated_at)
VALUES ($1, $2, NOW())
ON CONFLICT (user_id)
DO UPDATE SET
  email = EXCLUDED.email,
  updated_at = EXCLUDED.updated_at;
```

9. Keyset pagination (stable, scalable)  
Template:
```sql
SELECT id, created_at, payload
FROM events
WHERE (created_at, id) < ($last_created_at, $last_id)
ORDER BY created_at DESC, id DESC
LIMIT 50;
```

10. Conditional pivot for reporting  
Template:
```sql
SELECT user_id,
       SUM(amount) FILTER (WHERE status = 'success') AS success_amt,
       SUM(amount) FILTER (WHERE status = 'failed')  AS failed_amt
FROM txns
GROUP BY user_id;
```

Quick caveats:
- Add deterministic tie-breakers in `ORDER BY` (`id DESC`) for stable results.
- For deletes/updates, test with `SELECT` first or run inside transaction + rollback.
- Validate `NULL` behavior explicitly in anti-join and comparison queries.
