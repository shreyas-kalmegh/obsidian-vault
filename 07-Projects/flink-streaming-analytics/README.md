# Flink Streaming Analytics
Purpose: Real-time analytics pipeline using Flink to process streaming events, maintain state, and write enriched outputs to analytical stores.

Guidelines:
- Design stateful operators with RocksDB backend for large state.
- Use event-time processing and watermarks for correctness.
- Implement checkpointing and savepoints for controlled deployments.

Architecture.md
