# Kafka Offset Commit Protocol

## Overview
Offset commit is how a consumer group records progress. The committed offset is the next offset the group should read for a given topic-partition.

## Where Offsets Are Stored
- Kafka stores committed group offsets in the internal topic `__consumer_offsets`.
- The group coordinator handles commit and fetch requests.
- Offset commits are compacted because only the latest progress per group/topic/partition usually matters.

## Commit Modes
### Auto Commit
- Periodically commits the latest returned offsets.
- Simple, but risky if processing is slower than polling.

### Synchronous Commit
- Caller waits for broker acknowledgement.
- Higher latency, clearer failure handling.

### Asynchronous Commit
- Lower overhead.
- Caller must handle callback errors carefully.

## Processing Semantics
- Commit before processing: at-most-once
- Commit after processing: at-least-once
- Commit in transaction with output: exactly-once style pipeline

## Example
Consumer reads offsets `200` to `249`.

If it commits `250` before processing and then crashes:
- offsets `200` to `249` are lost from the application perspective

If it processes first and commits `250` after:
- crash before commit causes replay
- duplicates are possible, but loss is reduced

## Common Failure Cases
- Commit succeeds but app crashes before durable side effect.
- Rebalance occurs while processing old assignment.
- Async commit callback returns late and overwrites newer progress if coded poorly.

## Best Practices
- Commit only after work that must be preserved is finished.
- On rebalance, revoke handlers should flush work and commit carefully.
- Use external idempotency when writing to sinks outside Kafka.

## Interview Angle
- Committed offset means "resume here next," not "everything before this is permanently safe everywhere."
- Offset management is a correctness design choice, not just a consumer setting.
- `__consumer_offsets` being compacted is why old intermediate commits are not the main storage target.

## Related
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Consumer-Protocol.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Exactly-Once-Semantics.md]]
