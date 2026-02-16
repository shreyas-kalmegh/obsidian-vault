# Python Async Ingest Service
Purpose: Async service to ingest events from HTTP or websocket sources into Kafka or Kinesis.

Guidelines:
- Use asyncio and implement backpressure-aware ingestion.
- Validate and batch records before forwarding.
- Provide retry with exponential backoff and dead-letter handling.

Architecture.md
