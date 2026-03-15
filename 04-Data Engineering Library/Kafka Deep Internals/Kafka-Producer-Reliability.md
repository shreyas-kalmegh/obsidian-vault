# Kafka Producer Reliability

## Overview
Producer reliability is controlled by acknowledgements, retries, idempotence, replication health, and sometimes transactions. Reliable delivery is a combination of client and broker settings, not a single flag.

## Core Controls
- `acks=0`: fastest, weakest durability
- `acks=1`: leader-only acknowledgement
- `acks=all`: wait for required ISR acknowledgements
- `retries`: retry transient failures
- `enable.idempotence=true`: prevents retry duplicates per partition

## Idempotence Internals
- Broker assigns a producer ID.
- Producer sequence numbers increase per partition.
- Broker rejects duplicate sequence ranges.
- This prevents duplicates caused by retries after ambiguous failures.

## Reliability Matrix
- `acks=1` + retries:
  - still vulnerable to leader failure after acknowledgement but before replication
- `acks=all` + `min.insync.replicas >= 2`:
  - stronger durability
- idempotence + transactions:
  - needed for EOS-style stream processing

## Example
A produce request times out:
- leader actually wrote the batch
- ack never reached producer
- producer retries

Without idempotence, duplicate records may appear.  
With idempotence, the broker detects duplicate sequence numbers and suppresses the duplicate write.

## Operational Notes
- `acks=all` is only as strong as current ISR and `min.insync.replicas`.
- High retry rate can signal network instability or overloaded brokers.
- Out-of-order delivery risk rises if configs allow multiple in-flight requests without safe idempotence handling.

## Interview Angle
- Replication factor alone does not guarantee producer durability.
- Idempotence solves retry duplication, not atomic multi-partition workflows.
- Reliable producer settings often trade some latency for much better safety.

## Related
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-Exactly-Once-Semantics.md]]
- [[04-Data Engineering Library/Kafka Deep Internals/Kafka-ISR-Management.md]]
