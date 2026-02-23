# Indexes in RDBMS

## Table of Contents
- [What Is an Index](#what-is-an-index)
- [Why Indexes Matter](#why-indexes-matter)
- [Core Internals](#core-internals)
- [How Optimizers Use Indexes](#how-optimizers-use-indexes)
- [Types of Indexes](#types-of-indexes)
- [Clustered vs Non-Clustered](#clustered-vs-non-clustered)
- [When to Prefer Clustered vs Non-Clustered](#when-to-prefer-clustered-vs-non-clustered)
- [Composite and Covering Indexes](#composite-and-covering-indexes)
- [Selectivity, Cardinality, and Column Order](#selectivity-cardinality-and-column-order)
- [Write Costs and Tradeoffs](#write-costs-and-tradeoffs)
- [Index Management and Maintenance](#index-management-and-maintenance)
- [Practical Design Guidelines](#practical-design-guidelines)
- [PostgreSQL-Specific Notes](#postgresql-specific-notes)
- [Database Support Matrix](#database-support-matrix)

## What Is an Index
An index is a secondary data structure that helps the database locate rows faster than scanning the whole table.

- Think of it like a book index: jump to likely pages first, then fetch exact rows.
- Most relational engines use `B-tree`/`B+tree` indexes by default.
- Indexes speed reads but add storage and write overhead.

## Why Indexes Matter
- Reduce query latency for `WHERE`, `JOIN`, `ORDER BY`, and sometimes `GROUP BY`.
- Enable efficient point lookups and range scans.
- Help enforce constraints like `PRIMARY KEY` and `UNIQUE`.

## Core Internals
### B+Tree Structure
- `Root page`: top of tree.
- `Internal pages`: routing keys to child pages.
- `Leaf pages`: ordered key entries; point to row locations (or contain row data for clustered layouts).
- Tree height is usually small (often 2 to 4 levels), so lookups are near `O(log n)`.

### Page and Row Mechanics
- Data/indexes are stored in fixed-size pages.
- Inserts may trigger `page splits` when target pages are full.
- Splits can increase fragmentation and reduce locality.
- `Fill factor` reserves free space in pages to reduce split frequency.

### Row Pointer Behavior
- Non-clustered indexes usually store key + row locator.
- Row locator can be physical (heap pointer) or logical (clustered key), depending on engine design.

## How Optimizers Use Indexes
- Cost-based optimizers compare plans using table statistics.
- Common access patterns include `Index Seek`, `Index Range Scan`, `Index Scan`, and `Table/Heap Scan`.
- `Index Seek`: very selective lookup.
- `Index Range Scan`: scan key range.
- `Index Scan`: scan significant part of index.
- `Table/Heap Scan`: full scan when index is not beneficial.
- Sargable predicates (search-argument-able) are critical.
- Good: `col = 10`, `col BETWEEN 10 AND 20`, `col LIKE 'abc%'`.
- Often bad: `FUNCTION(col) = ...` unless using expression/function-based index.

## Types of Indexes
### By Data Structure
- `B-tree / B+tree`: default general-purpose index.
- `Hash`: equality lookups (`=`), not for ranges.
- `Bitmap` (engine-dependent): efficient for low-cardinality analytics filters.
- `GiST / SP-GiST` (PostgreSQL): generalized trees for geometric/text/search-like workloads.
- `GIN` (PostgreSQL): inverted index, great for arrays, jsonb, full-text style membership queries.
- `BRIN` (PostgreSQL): block-range summaries, very small and good for huge append-heavy tables with natural ordering.

### By Logical Behavior
- `Primary key index`: supports row identity.
- `Unique index`: enforces uniqueness.
- `Composite index`: multiple columns.
- `Covering index`: includes all columns needed by query, avoiding extra table lookups.
- `Partial/Filtered index`: index only rows matching predicate.
- `Expression/Function-based index`: index computed expression.
- `Clustered index`: defines physical row order (engine-specific behavior).
- `Non-clustered index`: separate structure from base table storage.

## Clustered vs Non-Clustered
### Key Difference
- Clustered index controls table row order on disk (or logical primary storage order).
- Non-clustered index stores separate key structure with references back to rows.

### Comparison
| Aspect | Clustered Index | Non-Clustered Index |
|---|---|---|
| Physical row order | Yes (or primary storage order) | No |
| Count per table | Usually one | Many |
| Lookup by key | Very fast | Fast |
| Range scans | Excellent | Good to excellent |
| Insert/update cost | Higher when key is random | Lower than clustered changes on base order |
| Storage | Base table organized by key | Additional separate storage |
| Best use | PK/range-heavy access paths | Additional query patterns |

### Important Caveat
- In PostgreSQL, tables are heap tables. `CLUSTER` rewrites table once to match an index order, but order is not maintained automatically after future writes.

## When to Prefer Clustered vs Non-Clustered
### Prefer Clustered Index When
- The table is frequently queried by range on one key (for example, time-series by `created_at`).
- You often need ordered scans (`ORDER BY`) on that key.
- The clustered key is stable and mostly increasing (reduces page splits).
- Workload is read-heavy and benefits from locality of related rows.

Typical examples:
- `orders` accessed by `(order_date)` ranges.
- `events` queried by `(event_time)` windows.
- Primary key lookups where PK is the dominant access path.

### Prefer Non-Clustered Index When
- You need multiple alternate lookup paths on the same table.
- Workload has many point lookups on different columns.
- The candidate key is random and would fragment clustered storage.
- You want covering behavior for specific query families.

Typical examples:
- Lookup by `email`, `phone`, `external_id` in addition to PK.
- Mixed query workloads with many different predicates.
- OLTP systems with frequent writes where clustered key changes are expensive.

### Rule of Thumb
- Pick one stable, high-value access path for clustered/primary storage ordering.
- Add targeted non-clustered indexes for other hot query patterns.
- Re-evaluate after workload or data-distribution changes.

## Composite and Covering Indexes
### Composite (Multi-column)
- Good when query filters/sorts on a predictable column prefix.
- Leftmost-prefix rule typically applies for B-tree usage.

Example:
```sql
CREATE INDEX idx_orders_customer_date
ON orders (customer_id, created_at);
```

### Covering
- Include select-list columns to avoid extra row fetches (engine features differ).
- In PostgreSQL, `INCLUDE` adds non-key columns to leaf tuples:

```sql
CREATE INDEX idx_orders_customer_date_inc
ON orders (customer_id, created_at)
INCLUDE (status, total_amount);
```

## Selectivity, Cardinality, and Column Order
- Prefer high-selectivity columns for leading index positions.
- Put most common equality filters early.
- Put range columns after equality columns in many workloads.
- Align index order with frequent `ORDER BY` to avoid sort operations.

## Write Costs and Tradeoffs
- Every insert/update/delete may update one or more indexes.
- More indexes can slow ingestion and increase lock/contention pressure.
- Random key inserts (e.g., UUID v4) can increase page splits and fragmentation.
- Wide indexes increase cache pressure and storage.

## Index Management and Maintenance
### Health Checks
- Track index usage stats (reads vs writes).
- Detect unused or duplicate indexes.
- Watch bloat/fragmentation and table/index size growth.

### Maintenance Operations
- Rebuild/reorganize/reindex depending on engine capabilities.
- Update optimizer statistics (`ANALYZE` or equivalent).
- Vacuum/cleanup dead tuples where MVCC engines require it.
- Consider concurrent/online index operations in production.

### Fragmentation (Concept)
- Fragmentation means logical key order no longer maps cleanly to physical page order.
- Effects: more random IO, poorer cache locality, larger trees, slower range scans.
- Mitigation: proper fill factor, periodic maintenance, better key patterns, partitioning.

## Practical Design Guidelines
- Start from query patterns, not from table definitions alone.
- Add indexes for high-value `WHERE` + `JOIN` paths first.
- Avoid indexing every column.
- Validate with real plans (`EXPLAIN`/`EXPLAIN ANALYZE`).
- Remove indexes that are unused and expensive to maintain.
- Revisit index strategy after data volume/query shape changes.

## PostgreSQL-Specific Notes
- Default index type is `B-tree`.
- Supported methods: `btree`, `hash`, `gin`, `gist`, `spgist`, `brin`.
- `PRIMARY KEY` and `UNIQUE` create backing unique indexes.
- Partial index example:

```sql
CREATE INDEX idx_customer_active
ON customer (last_login_at)
WHERE active = true;
```

- Expression index example:

```sql
CREATE INDEX idx_user_email_lower
ON users ((lower(email)));
```

- Reindex options: `REINDEX INDEX index_name;`, `REINDEX TABLE table_name;`, `REINDEX DATABASE db_name;`

- Inspect indexes:

```sql
SELECT schemaname, tablename, indexname, indexdef
FROM pg_indexes
ORDER BY schemaname, tablename, indexname;
```

## Database Support Matrix
Legend:
- `Native`: first-class support.
- `Partial`: supported with constraints/limitations.
- `N/A`: not supported as a first-class index type.

| Database | Clustered Storage/Index | Non-Clustered | B-tree | Hash | Bitmap | GIN | GiST / SP-GiST | BRIN | Partial/Filtered | Expression/Function | Full-Text Related |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PostgreSQL | Partial (`CLUSTER` is one-time reorder, heap remains) | Native | Native | Native | N/A | Native | Native | Native | Native (partial index) | Native | Native (`GIN/GiST` for FTS) |
| MySQL (InnoDB) | Native (clustered by PK) | Native (secondary indexes) | Native | N/A (engine-level adaptive hash is internal) | N/A | N/A | N/A | N/A | Partial (via generated columns/prefix patterns, no true filtered index) | Partial (functional indexes in MySQL 8+) | Native (`FULLTEXT`) |
| SQL Server | Native (clustered index) | Native | Native | N/A | Native | N/A | N/A | N/A | Native (filtered index) | Native | Native (full-text indexes) |
| Oracle | Partial (IOT tables; heap default) | Native | Native | N/A | Native | N/A | N/A | N/A | Native (function-based + predicate strategies) | Native (function-based index) | Native (Oracle Text) |
| SQLite | N/A (rowid table model, no classic clustered index knob) | Native | Native | N/A | N/A | N/A | N/A | N/A | Partial (partial index supported) | Native (expression index) | Partial (via FTS virtual tables) |

Notes:
- Terminology differs by engine; “clustered” may describe table organization rather than a separate index type.
- Full-text indexing is often a separate subsystem from classic B-tree indexing.
