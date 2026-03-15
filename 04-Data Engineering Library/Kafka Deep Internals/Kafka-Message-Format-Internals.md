# Kafka Message Format Internals

## Overview
Kafka no longer stores messages as isolated records on disk. It stores record batches. This reduces overhead, improves compression, and aligns storage and network transfer around batches instead of single events.

## Hierarchy Context
```text
Topic Partition
  -> Segment
    -> Record Batch
      -> Record
```

- Batches live inside segment `.log` files.
- A batch is not the same thing as a segment.
- Kafka appends many batches to the active segment before rolling a new segment.

## Record Batch Concepts
- A batch contains one or more records.
- Batch metadata includes base offset, magic version, timestamps, CRC, compression type, and producer state if idempotence or transactions are used.
- Individual records inside the batch use relative offsets and compact encodings.

## Important Fields
- `magic`: record format version
- `baseOffset`: first offset in the batch
- `baseTimestamp`: anchor timestamp
- `attributes`: compression, timestamp type, transactional flag, control batch flag
- `producerId`, `producerEpoch`, `baseSequence`: used for idempotence and transactions

## Example
One compressed batch may contain 500 records:
- offsets `1000` to `1499`
- producer ID `321`
- sequence range used to detect retry duplicates
- compression `lz4`

Broker writes and replicates the batch as a unit, not 500 independent disk records.

## Why Batching Matters
- Better compression ratio
- Fewer syscalls and network requests
- Lower per-message protocol overhead
- Faster sequential disk IO

## Timestamps
- `CreateTime`: set by producer
- `LogAppendTime`: set by broker
- Timestamp type affects retention policies, stream-time semantics, and debugging

## Compression
- Compression is applied at batch level.
- Common choices:
  - `snappy`: balanced
  - `lz4`: strong throughput choice
  - `zstd`: strong compression efficiency, often higher CPU cost
  - `gzip`: usually slower

## Interview Angle
- Kafka’s wire and disk format are optimized for batches, not individual event mutation.
- Magic/version evolution enables broker compatibility across format changes.
- Producer sequence numbers live in batch metadata because reliability is batch-aware.

## Related
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Producer-Internals.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Producer-Reliability.md]]
