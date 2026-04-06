# Log Parsing And Processing Interview Question

## Question
You are given an application log file stored as plain text. Each line looks like:

```text
2026-03-16 10:15:23 INFO user_id=42 endpoint=/checkout latency_ms=120 status=200
2026-03-16 10:15:25 ERROR user_id=42 endpoint=/checkout latency_ms=980 status=500
2026-03-16 10:15:27 INFO user_id=77 endpoint=/home latency_ms=45 status=200
```

Write code to:
- parse the log lines
- ignore malformed rows
- calculate request count by endpoint
- calculate average latency by endpoint
- calculate error count where `status >= 500`

In an interview, I would mention two approaches:
- `pandas` if speed of development matters and the file fits comfortably in memory
- Python standard library if dependencies should stay minimal or if I want tighter control over streaming row-by-row parsing

## Approach 1: `pandas`

```python
import pandas as pd

def parse_log_with_pandas(path: str) -> pd.DataFrame:
    rows = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 7:
                continue

            try:
                timestamp = f"{parts[0]} {parts[1]}"
                level = parts[2]
                user_id = int(parts[3].split("=", 1)[1])
                endpoint = parts[4].split("=", 1)[1]
                latency_ms = int(parts[5].split("=", 1)[1])
                status = int(parts[6].split("=", 1)[1])
            except (IndexError, ValueError):
                continue

            rows.append(
                {
                    "timestamp": timestamp,
                    "level": level,
                    "user_id": user_id,
                    "endpoint": endpoint,
                    "latency_ms": latency_ms,
                    "status": status,
                }
            )

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    summary = (
        df.groupby("endpoint", as_index=False)
        .agg(
            request_count=("endpoint", "size"),
            avg_latency_ms=("latency_ms", "mean"),
            error_count=("status", lambda s: (s >= 500).sum()),
        )
        .sort_values("request_count", ascending=False)
    )

    return summary
```

### When I Would Choose `pandas`
- the file is medium-sized and fits in memory
- I want concise aggregation code
- I may later extend the solution into richer analysis or export

### Tradeoffs
- simpler code for aggregation
- higher memory usage
- dependency on `pandas`

## Approach 2: Python Standard Library

```python
from collections import defaultdict


def parse_log_with_stdlib(path: str) -> list[dict]:
    request_count = defaultdict(int)
    latency_sum = defaultdict(int)
    error_count = defaultdict(int)

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 7:
                continue

            try:
                endpoint = parts[4].split("=", 1)[1]
                latency_ms = int(parts[5].split("=", 1)[1])
                status = int(parts[6].split("=", 1)[1])
            except (IndexError, ValueError):
                continue

            request_count[endpoint] += 1
            latency_sum[endpoint] += latency_ms
            if status >= 500:
                error_count[endpoint] += 1

    result = []
    for endpoint, count in request_count.items():
        result.append(
            {
                "endpoint": endpoint,
                "request_count": count,
                "avg_latency_ms": latency_sum[endpoint] / count,
                "error_count": error_count[endpoint],
            }
        )

    return sorted(result, key=lambda row: row["request_count"], reverse=True)
```

### When I Would Choose Standard Library
- I want streaming-friendly processing
- the file may be large
- I do not want external dependencies
- I only need fixed aggregations

### Tradeoffs
- more manual code
- better memory efficiency
- easier to reason about row-by-row validation

## Interview Discussion Points
- For truly large log volumes, I would not use single-node `pandas`; I would move to Spark, Flink, or a streaming pipeline.
- I would define malformed-row handling explicitly so the parser is robust in production.
- If order matters, I would preserve timestamp parsing with `datetime`.
- If schema drift is common, regex or structured logging formats like JSON are safer than positional parsing.

## Strong Follow-Up Questions
### How would you handle logs too large for memory?
I would process them in a streaming fashion, aggregate incrementally, or move the workload to Spark if distributed processing is needed.

### What if logs arrive continuously instead of as a file?
I would model it as a streaming problem with Kafka plus Spark Structured Streaming or Flink, and compute rolling aggregates.

### How would you handle malformed rows in production?
I would count and quarantine them, emit metrics, and store a sample for debugging instead of silently dropping everything.

### What if the logs were JSON?
I would prefer JSON because parsing is safer and schema evolution is easier to manage than ad hoc string splitting.

### How would you optimize this further?
I would avoid repeated string splits, benchmark parsing cost, batch reads, and move to columnar or distributed processing once file volume justifies it.
