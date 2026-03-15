# Flink -> MSK -> Pinot Hybrid Example

This folder extends the Flink repartition job with Pinot hybrid-table configs.

## Flow

1. Flink reads raw orders from source Kafka.
2. Flink repartitions by `id`, writes to MSK topic `orders-by-id`.
3. Late events are routed by Flink to `orders-late`.
4. Pinot REALTIME table ingests `orders-by-id`.
5. Pinot OFFLINE table stores batch/backfill segments for the same logical table (`orders_hybrid`).
6. Optional replay job consumes `orders-late` and replays eligible events back to `orders-by-id`.

## Files

- `orders_schema.json`: Pinot schema with `order_id` primary key.
- `orders_realtime_table.json`: REALTIME config reading from MSK.
- `orders_offline_table.json`: OFFLINE config for hybrid table.
- `replay_late_orders_to_msk.py`: Flink replay job for late events.

## Register in Pinot

```bash
pinot-admin.sh AddSchema -schemaFile orders_schema.json -exec
pinot-admin.sh AddTable -tableConfigFile orders_realtime_table.json -exec
pinot-admin.sh AddTable -tableConfigFile orders_offline_table.json -exec
```

## Late-arriving data strategy

- In Flink: late events are detected using `event_time_ms` and sent to `orders-late` for remediation/replay.
- In Pinot: `upsertConfig.comparisonColumns = ["event_time_ms"]` keeps the newest event per `order_id`.
- For backfills: ingest corrected historical data into OFFLINE segments, then reload/refresh table.

## Replay late events

Replay rules in `replay_late_orders_to_msk.py`:
- Event must include `id`/`order_id`.
- If `replay_allowed` exists and is `false`, skip replay.
- Event age (`now - event_time_ms`) must be within `--max-replay-age-seconds`.
- Replayed events are enriched with `replay_time_ms` and `replayed_from`.
- Rejected events go to `orders-late-rejected`.

Run:

```bash
python replay_late_orders_to_msk.py \
  --source-bootstrap-servers "<MSK_BROKERS>" \
  --sink-bootstrap-servers "<MSK_BROKERS>" \
  --source-topic "orders-late" \
  --sink-topic "orders-by-id" \
  --reject-topic "orders-late-rejected" \
  --max-replay-age-seconds 604800
```
