# Pinot Upserts And Dedup

## Overview
Pinot is primarily built for immutable analytical data, but it also supports deduplication and upserts for workloads where newer records should replace older ones. This is useful for mutable entities, CDC-like streams, and event corrections, but it introduces extra state-management cost.

## Dedup
- Dedup keeps only the first version of a primary-keyed record that arrives.
- It is useful when retry duplicates are common and later records should not replace earlier ones.

## Upserts
- Upserts keep the latest record for a primary key based on a comparison field such as event time or sequence number.
- Queries should see only the most current valid version.

## How It Works At A High Level
- Pinot tracks primary-key state.
- New records are compared against the currently known version.
- Older superseded rows are masked from query results.

## Example
User profile stream:
- record 1: `user_id=42`, plan=`free`, ts=`100`
- record 2: `user_id=42`, plan=`pro`, ts=`120`

With upsert enabled, queries should return only the `pro` version as the latest visible state.

## Tradeoffs
- Better support for mutable analytical entities
- Additional memory and metadata overhead
- More complexity during recovery and segment replacement

## Operational Notes
- Primary key choice matters a lot.
- Out-of-order events require a reliable comparison column.
- Upsert tables need closer memory monitoring than append-only tables.

## Interview Angle
- Upserts make Pinot more flexible, but they are not free.
- Pinot still thinks in segments, so mutable semantics are layered on top of an analytics engine.
- If full transactional update semantics are needed, Pinot is usually not the right primary system.

## Related
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Realtime-Ingestion-and-Segment-Commit.md]]
- [[04-Data Engineering Library/Pinot Deep Internals/Pinot-Monitoring-KPIs.md]]
