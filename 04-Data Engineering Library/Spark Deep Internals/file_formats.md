# Spark File Formats: What To Use, When, and Caveats

## Quick decision guide

| Use case | Recommended format | Why |
|---|---|---|
| General analytics table on data lake | Parquet | Columnar, compressed, predicate pushdown, broad ecosystem support |
| Lakehouse table with ACID + schema evolution + upserts/deletes | Delta Lake / Apache Iceberg / Apache Hudi | Transaction log + snapshot isolation + time travel |
| High-performance analytics in some engines with advanced metadata indexing | ORC | Strong compression/encoding; common in Hive ecosystems |
| Simple row-oriented export or interoperability | CSV | Human-readable and universally portable |
| Semi-structured logs/events | JSON | Flexible schema, easy ingestion |
| Binary compact row format (streaming, RPC pipelines) | Avro | Schema evolution with schema registry patterns |
| Fast external extract + small/medium interchange | Arrow (in-memory), not long-term lake storage | Zero-copy columnar transfer for UDF/Pandas interop |
| Raw ingest from Kafka/event bus for replay | text/JSON/Avro in bronze, then normalize to Parquet/lakehouse table | Keep raw fidelity, optimize downstream reads |

## Formats Spark supports commonly

- Built-in/common read-write: `parquet`, `orc`, `json`, `csv`, `text`, `avro` (module/package may be needed depending on Spark distro/version).
- Table/lakehouse formats through connectors: Delta, Iceberg, Hudi.
- Compression codecs across formats: `snappy` (default common), `zstd`, `gzip`, `lz4` depending on format and cluster support.

## Format-by-format notes

### 1) Parquet
Use when:
- Most analytical workloads on object storage/data lake.
- Wide tables where column pruning helps.

Why:
- Columnar layout + stats + predicate pushdown.
- Usually best default for Spark SQL performance.

Gotchas:
- Many tiny files kill performance (metadata + scheduling overhead).
- Schema merge can be expensive (`mergeSchema`).
- Poor partition design causes skew and high small-file counts.
- Over-partitioning by high-cardinality columns is a common anti-pattern.

### 2) ORC
Use when:
- Hive-heavy ecosystem or ORC-optimized downstream stack.
- Need strong compression and vectorized reads in compatible engines.

Gotchas:
- Ecosystem/tooling often less universal than Parquet in mixed stacks.
- Cross-engine behavior can differ around complex types and settings.

### 3) Delta / Iceberg / Hudi (table formats, not just file formats)
Use when:
- You need ACID transactions, reliable upserts/deletes, schema evolution, and time travel.

Why:
- Avoids many “raw Parquet table” failure modes (partial overwrite, consistency issues, no transaction log).

Gotchas:
- Extra metadata + maintenance operations required (`OPTIMIZE`, compaction, snapshot cleanup/vacuum/expire snapshots depending on format).
- Need compatible Spark runtime + connector versions.
- Object-store + catalog configuration is part of correctness.

### 4) JSON
Use when:
- Raw event landing, schema-on-read, variable payloads.

Gotchas:
- Row-oriented and verbose; expensive for heavy analytics.
- Type inference can be slow/inconsistent at scale.
- Nested/variant fields can drift and break downstream jobs unless controlled.

### 5) CSV
Use when:
- Data interchange with external tools/business users.

Gotchas:
- No native schema/types; everything starts as text.
- Quoting/escaping/newlines/encoding issues are frequent.
- Slow for analytics and very large datasets.

### 6) Avro
Use when:
- Event pipelines, schema evolution contracts, Kafka integration.

Gotchas:
- Row-oriented, so analytics scans are usually slower than Parquet/ORC.
- Requires schema discipline; evolution rules must be managed carefully.

### 7) Text
Use when:
- Raw logs or unstructured records.

Gotchas:
- No structure, no pushdown, no type safety.
- Usually staging-only before parse/normalize.

## Spark-specific caveats that matter more than format choice

- File size target: aim for reasonably large files (commonly ~128MB to 1GB depending on workload/storage).
- Small-files problem: compact periodically or use optimized writes.
- Partitioning strategy:
  - Partition by low/medium cardinality query filters (e.g., date).
  - Avoid partitioning on highly unique columns (user_id/order_id).
- Compression tradeoffs:
  - `snappy`: faster read/write, common default.
  - `zstd`/`gzip`: better compression, can cost more CPU.
- Schema evolution:
  - Define explicit schemas for JSON/CSV where possible.
  - Treat renames/type-changes carefully; they are harder than additive columns.
- Predicate pushdown and pruning only help if filters align with stats/partition columns.
- Object storage consistency/rename behavior can impact write patterns; table formats reduce risk.

## Practical recommendations

1. Default to Parquet for analytics datasets unless you need ACID table semantics.
2. Use Delta/Iceberg/Hudi for curated tables that need updates/deletes/CDC correctness.
3. Keep JSON/CSV/Avro mostly at ingestion boundaries; convert to columnar for query layers.
4. Optimize file sizes and partitioning early; this often gives bigger gains than codec tweaking.
5. Standardize one or two table formats in your platform to reduce operational complexity.

## Interview Style Q&A

### Q1) What file format should you choose by default for Spark analytics and why?
**Answer:** Parquet. It is columnar, supports predicate pushdown and column pruning, and is broadly supported across engines.

### Q2) When would you choose Delta/Iceberg/Hudi over plain Parquet?
**Answer:** When you need ACID transactions, upserts/deletes, time travel, and reliable concurrent writes. Plain Parquet lacks transactional guarantees.

### Q3) Parquet vs ORC in Spark: what is the practical answer?
**Answer:** Both are columnar and performant. Parquet is usually the default in mixed ecosystems; ORC is often preferred in Hive-centric stacks.

### Q4) Why are JSON and CSV not ideal for large analytical tables?
**Answer:** They are row-oriented and text-heavy, have weaker typing, and are more expensive to scan and parse at scale.

### Q5) What is the “small files problem” and why does it hurt Spark jobs?
**Answer:** Too many small files increase metadata/listing overhead and task scheduling overhead, reducing throughput significantly.

### Q6) What file size target is commonly recommended for Spark lake data?
**Answer:** Roughly 128MB to 1GB per file, tuned by workload and storage system.

### Q7) What is a common partitioning mistake?
**Answer:** Partitioning by high-cardinality columns (like `order_id` or `user_id`), which creates too many tiny partitions/files.

### Q8) Which columns are good partition candidates?
**Answer:** Low/medium-cardinality columns frequently used in filters, usually date/time-derived columns.

### Q9) What are common compression choices in Spark and how do you choose?
**Answer:** `snappy` for balanced speed; `zstd`/`gzip` for better compression at higher CPU cost.

### Q10) What is schema evolution, and what is the safe strategy in practice?
**Answer:** Changing table schema over time. Additive changes are safest; renames/type changes require careful migration planning.

### Q11) Why explicitly define schema for JSON/CSV reads?
**Answer:** It avoids expensive/inconsistent inference and prevents downstream type drift issues.

### Q12) Where does Avro fit in a Spark data platform?
**Answer:** Best at ingestion/event boundaries (e.g., Kafka + schema evolution), then usually converted to Parquet/table format for analytics.

### Q13) If a table needs frequent updates and deletes, what do you recommend?
**Answer:** A lakehouse table format (Delta/Iceberg/Hudi) with proper compaction and metadata maintenance.

### Q14) Is format choice alone enough for good performance?
**Answer:** No. File sizing, partitioning, clustering/sorting, and table maintenance often matter as much or more.

### Q15) One-line production rule of thumb?
**Answer:** Ingest flexibly (JSON/Avro), curate in transactional table format if needed, and serve analytics from optimized columnar data.
