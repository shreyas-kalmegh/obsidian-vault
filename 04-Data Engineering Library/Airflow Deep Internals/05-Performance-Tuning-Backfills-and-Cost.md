# Performance Tuning, Backfills, and Cost

## Overview
Airflow performance tuning is usually queue/scheduler tuning plus workload shaping. The objective is stable throughput with predictable run latency, not maximum theoretical parallelism.

## High-Impact Levers

1. Scheduler and parse health
- Keep DAG files lightweight at import time.
- Avoid network calls at module import.
- Reduce expensive dynamic DAG generation logic.

2. Concurrency tuning
- Tune `parallelism`, `max_active_runs`, DAG/task limits.
- Use pools to protect expensive or rate-limited systems.

3. Worker/executor sizing
- Match worker slots to real external system capacity.
- More workers without downstream capacity just moves bottleneck.

## Backfill Strategy

Bad pattern:
- Launch huge historical backfill with same resources/queues as critical daily jobs.

Better pattern:
1. Separate backfill queue/pool.
2. Cap `max_active_runs` for backfill DAG.
3. Use chunked date windows.
4. Pause/resume based on warehouse/API pressure.

## Example: Controlled Backfill CLI

```bash
airflow dags backfill orders_daily_pipeline \
  --start-date 2025-01-01 \
  --end-date 2025-01-07 \
  --reset-dagruns
```

Operational note:
- Prefer small windows first, validate outputs, then scale range.

## Cost Signals to Track
- Task runtime percentile (`p50`, `p95`) by DAG.
- Retries per DAG and per dependency.
- Queue wait time (`scheduled -> running` latency).
- External engine spend correlated to Airflow run cadence.

## Example Incident Pattern
Symptom:
- Daily SLA miss, many tasks stuck `queued`.

Likely causes:
- Worker saturation
- Pool slot starvation
- Executor connectivity issues

First checks:
1. Queue depth and worker slot utilization.
2. Pool usage and blocked tasks.
3. Scheduler heartbeat and metadata DB latency.

## Common Tuning Mistakes
- Over-tuning config knobs before fixing DAG/task design.
- Ignoring parse-time overhead from heavy imports.
- High schedule frequency for pipelines with long end-to-end runtime.
- Letting backfills compete with real-time/business-critical jobs.
