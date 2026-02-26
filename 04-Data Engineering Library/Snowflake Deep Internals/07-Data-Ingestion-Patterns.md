# Data Ingestion Patterns

## Core ingestion options
1. Batch file loads with `COPY INTO`
2. Continuous file ingestion with Snowpipe
3. Streaming ingestion patterns (tool- or connector-driven)

Choose based on latency requirements and operational overhead.

## Stages and file formats
Snowflake loads data from internal/external stages.

Best practices:
- Standardize file format objects (CSV/JSON/Parquet settings).
- Keep raw landing immutable.
- Track source metadata (filename, load timestamp, batch id).

## COPY INTO practicals
- Use explicit column mapping when possible.
- Capture load status using load history and metadata tables.
- Handle bad records with controlled error strategy (`ON_ERROR` depending on SLA).

## Snowpipe usage guidance
Good fit for near-real-time ingestion of arriving files.

Considerations:
- Event-driven setup depends on cloud provider integration.
- Monitor pipe lag and error events.
- Cost is tied to event volume and processing behavior.

## Idempotency and deduplication
Ingestion pipelines should tolerate retries.

Common pattern:
- Land raw data with ingestion metadata.
- Deduplicate into staging using natural/business keys plus event/update timestamp.

## Schema evolution
- Semi-structured sources evolve frequently.
- Use staged parsing and controlled projection into typed tables.
- Avoid exposing raw variant directly to BI users.
