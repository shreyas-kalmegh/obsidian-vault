# Python Concurrency: Practical Notes

## Quick Reference Table

| Model | Best For | Core Tooling | Caveat |
|---|---|---|---|
| Threads | I/O-bound work (HTTP, DB, files) | `threading`, `ThreadPoolExecutor` | GIL limits CPU parallelism |
| Async IO | High-concurrency network services | `asyncio`, `aiohttp`, async DB clients | Must use non-blocking libraries |
| Processes | CPU-bound work | `multiprocessing`, `ProcessPoolExecutor` | Higher memory + serialization overhead |
| Queues/Pipelines | Producer-consumer workflows | `queue.Queue`, `asyncio.Queue`, `multiprocessing.Queue` | Backpressure design required |

---

## 1) Concurrency vs Parallelism

- Concurrency: tasks make progress during overlapping time.
- Parallelism: tasks execute at the same instant (multiple cores/processes).

Python rule of thumb:
- I/O-bound -> threads or asyncio
- CPU-bound -> processes

---

## 2) GIL in One Minute

- CPython GIL allows only one thread to execute Python bytecode at a time.
- Threads still help when waiting on I/O because the GIL is released while blocked.
- For pure CPU loops, use `multiprocessing`/process pools for real parallel speedup.

---

## 3) Threading Basics

```python
import threading
import time


def worker(name):
    time.sleep(0.2)  # I/O wait simulation
    print(f"done: {name}")


t1 = threading.Thread(target=worker, args=("A",))
t2 = threading.Thread(target=worker, args=("B",))
t1.start(); t2.start()
t1.join(); t2.join()
```

Gotchas:
- Shared mutable state can race.
- Always `join()` non-daemon threads for clean shutdown.

---

## 4) Race Condition + Lock (Minimal Correct Pattern)

```python
import threading

counter = 0
lock = threading.Lock()


def inc(n):
    global counter
    for _ in range(n):
        with lock:
            counter += 1
```

Why:
- `counter += 1` is not atomic at Python bytecode level.

Gotchas:
- Keep lock scope small.
- Do not call long/blocking operations while holding a lock.

---

## 5) Complex Case: Deadlock Avoidance

```python
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()

# Good: always acquire locks in same global order

def safe_fn():
    first, second = (lock_a, lock_b)
    with first:
        with second:
            pass
```

Deadlock risk appears when two paths acquire `A->B` and `B->A`.

Mitigation:
- Consistent lock ordering
- Timeouts (`lock.acquire(timeout=...)`)
- Fewer locks / immutable data when possible

---

## 6) Producer-Consumer with `queue.Queue`

```python
from queue import Queue
from threading import Thread

q = Queue(maxsize=100)  # maxsize adds backpressure


def producer(items):
    for item in items:
        q.put(item)
    q.put(None)  # sentinel


def consumer():
    while True:
        item = q.get()
        if item is None:
            q.task_done()
            break
        # process item
        q.task_done()

Thread(target=consumer).start()
Thread(target=producer, args=([1, 2, 3],)).start()
q.join()
```

Why this matters:
- `maxsize` prevents unbounded memory growth.

---

## 7) `ThreadPoolExecutor` Pattern

```python
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch(x):
    return x * 2

with ThreadPoolExecutor(max_workers=8) as ex:
    futures = [ex.submit(fetch, i) for i in range(20)]
    for f in as_completed(futures):
        print(f.result())
```

Gotchas:
- Too many workers can degrade performance.
- Exceptions surface on `future.result()`.

---

## 8) Async IO Basics (`asyncio`)

```python
import asyncio


async def fetch(i):
    await asyncio.sleep(0.2)  # non-blocking wait
    return i * 10


async def main():
    results = await asyncio.gather(*(fetch(i) for i in range(5)))
    print(results)

asyncio.run(main())
```

Gotchas:
- Do not call blocking functions directly in async code.
- Use async-native clients (`aiohttp`, async DB drivers).

---

## 9) Complex Case: Mix Async + Blocking Work Safely

If inside async code you must run blocking CPU/file calls:

```python
import asyncio


def blocking_fn(x):
    # CPU-heavy or blocking library call
    return x * x


async def main():
    loop = asyncio.get_running_loop()
    val = await loop.run_in_executor(None, blocking_fn, 10)
    print(val)
```

Why:
- Prevents event loop stalls and latency spikes.

---

## 10) Timeouts and Cancellation (Production Critical)

```python
import asyncio


async def slow():
    await asyncio.sleep(5)
    return "ok"


async def main():
    try:
        result = await asyncio.wait_for(slow(), timeout=1.0)
        print(result)
    except asyncio.TimeoutError:
        print("timed out")

asyncio.run(main())
```

Notes:
- Cancellation is cooperative: tasks must hit `await` points.
- Use `try/finally` in coroutines to release resources on cancellation.

---

## 11) Multiprocessing for CPU-Bound Tasks

```python
from concurrent.futures import ProcessPoolExecutor


def cpu_task(x):
    total = 0
    for i in range(2_000_000):
        total += (i ^ x) & 7
    return total


if __name__ == "__main__":
    with ProcessPoolExecutor() as ex:
        results = list(ex.map(cpu_task, [1, 2, 3, 4]))
    print(results)
```

Gotchas:
- Protect entrypoint with `if __name__ == "__main__":`.
- Functions/args must be picklable.
- Large object transfer between processes is expensive.

---

## 12) Shared State Across Processes

Options:
- Prefer message passing (`multiprocessing.Queue`) over shared mutables.
- Use `multiprocessing.Value/Array` for simple primitives.
- Use shared memory only when profiling justifies complexity.

Guideline:
- Minimize cross-process communication volume.

---

## 13) Choosing the Right Model

- Many network calls / scraping: `asyncio` or thread pool
- Existing sync code + moderate I/O: `ThreadPoolExecutor`
- Heavy CPU compute: `ProcessPoolExecutor`
- Multi-stage ingestion pipeline: queue-based producer/consumer
- Low-latency service: async + strict timeouts + backpressure

---

## 14) Same Problem, Different Models

Problem: fetch many URLs and parse a small response.

### A) Sequential (baseline)
```python
import requests

urls = ["https://example.com"] * 100
results = [requests.get(u, timeout=5).status_code for u in urls]
```

When to use:
- Small workloads, simplest debugging path.

### B) ThreadPool (same sync library, better I/O overlap)
```python
import requests
from concurrent.futures import ThreadPoolExecutor


def fetch_status(url):
    return requests.get(url, timeout=5).status_code


urls = ["https://example.com"] * 100
with ThreadPoolExecutor(max_workers=20) as ex:
    results = list(ex.map(fetch_status, urls))
```

When to use:
- Existing synchronous codebase, mostly network/file/database wait.

### C) Async IO (best for very high I/O fan-out)
```python
import asyncio
import aiohttp


async def fetch_status(session, url):
    async with session.get(url, timeout=5) as resp:
        return resp.status


async def main():
    urls = ["https://example.com"] * 100
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_status(session, u) for u in urls]
        results = await asyncio.gather(*tasks)
        print(results[:5])

asyncio.run(main())
```

When to use:
- Large number of concurrent sockets and async-native dependencies.

### D) If workload becomes CPU-bound after fetch
Use process pool for the heavy transform stage:

```python
from concurrent.futures import ProcessPoolExecutor


def heavy_parse(raw_text):
    # CPU-heavy parsing/scoring
    return sum(ord(c) for c in raw_text) % 1000


with ProcessPoolExecutor() as ex:
    scores = list(ex.map(heavy_parse, big_text_blobs))
```

Rule:
- I/O stage: threads/async
- CPU stage: processes

---

## 15) High-Value Gotchas

- Assuming threads speed up CPU-bound Python code (GIL says usually no).
- Forgetting timeouts -> stuck workers and tail-latency incidents.
- Unbounded queues -> memory blowups under load.
- Holding locks during I/O -> throughput collapse.
- Swallowing exceptions in worker threads/tasks.
- Using blocking libs in async code (`requests`, blocking DB clients).
- Process pool with non-picklable callables (nested/lambda often fail).

---

## 16) Interview/Design Sound Bites

- "I/O-bound: overlap waits with threads/async. CPU-bound: use processes."
- "Add backpressure (`maxsize`) so producers cannot outrun consumers."
- "Use timeouts + cancellation + cleanup (`finally`) for resilient concurrency."
- "Prefer message passing over shared mutable state to reduce race complexity."
