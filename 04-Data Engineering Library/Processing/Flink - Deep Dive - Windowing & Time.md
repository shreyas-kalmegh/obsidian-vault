# Flink Deep Dive — Windowing, Time Semantics, and Late Data

## Windowing models
- Tumbling windows: fixed-size, non-overlapping windows.
- Sliding windows: windows that slide by a step, possibly overlapping.
- Session windows: dynamic windows separated by gaps of inactivity.

## Event time vs processing time
- Event time: time from data itself; requires watermarks and is robust to irregular arrivals.
- Processing time: system time when events are processed; simpler but less accurate for real-world streams.

## Late data handling
- Watermark strategies: periodic vs punctuated
- Allowed lateness: keep window state after watermark to accept late events
- Side outputs: route late events to a separate stream for analysis or reprocessing
