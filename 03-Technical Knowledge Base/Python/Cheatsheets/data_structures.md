# Python Data Structures: Practical Notes

## Quick Complexity Table

| Structure | Ordered? | Mutable? | Avg Lookup | Avg Insert/Delete | Notes |
|---|---|---|---|---|---|
| `list` | Yes (index order) | Yes | `O(1)` by index, `O(n)` by value | append/pop end `O(1)`, middle `O(n)` | Dynamic array |
| `tuple` | Yes | No | `O(1)` by index | N/A | Hashable if all items hashable |
| `set` | No (insertion-preserving in CPython, but do not rely semantically) | Yes | `O(1)` avg | `O(1)` avg | Unique elements only |
| `dict` | Yes (insertion order, Python 3.7+) | Yes | `O(1)` avg | `O(1)` avg | Key-value hash table |
| `collections.deque` | Yes | Yes | ends `O(1)` | ends `O(1)` | Fast queue/stack both ends |
| `heapq` (list-backed) | Partial order (min at index 0) | Yes | min `O(1)` | push/pop `O(log n)` | Priority queue primitive |

---

## 1) `list`

Use for: dynamic arrays, iteration, stack (`append`/`pop`).

```python
nums = [10, 20, 30]
nums.append(40)         # [10, 20, 30, 40]
nums.pop()              # 40
nums.insert(1, 15)      # O(n)
nums.remove(20)         # remove by value, O(n)
```

Gotchas:
- `pop(0)` is `O(n)` (shifts all elements). Use `deque` for queue behavior.
- `[[0] * 3] * 2` shares inner list references.

```python
bad = [[0] * 3] * 2
bad[0][0] = 99          # both rows change

good = [[0] * 3 for _ in range(2)]
```

---

## 2) `tuple`

Use for: fixed records, dictionary keys, returning multiple values.

```python
point = (3, 5)
x, y = point
```

Gotchas:
- Single-element tuple needs trailing comma: `(1,)`.
- Tuple is immutable, but can contain mutable objects.

---

## 3) `set`

Use for: deduplication, fast membership, set algebra.

```python
s = {1, 2, 3}
s.add(4)
2 in s                  # True
s2 = {3, 4, 5}
union = s | s2
inter = s & s2
```

Gotchas:
- Elements must be hashable (`list` not allowed, `tuple` allowed if hashable contents).
- Set iteration order should not be treated as business logic.

---

## 4) `dict`

Use for: indexing, counting, grouping, caches.

```python
user = {"id": 1, "name": "ana"}
user["email"] = "ana@example.com"
name = user.get("name", "unknown")
```

Gotchas:
- `d[missing]` raises `KeyError`; use `get`, `setdefault`, or `defaultdict`.
- Insertion order is preserved (Python 3.7+), but sorting still requires explicit `sorted(...)`.

### Common dict patterns

```python
# Frequency count
freq = {}
for x in [1, 2, 2, 3]:
    freq[x] = freq.get(x, 0) + 1

# Grouping
groups = {}
for word in ["eat", "tea", "tan"]:
    k = ''.join(sorted(word))
    groups.setdefault(k, []).append(word)
```

---

## 5) `collections.deque`

Use for: queues, BFS, sliding window indices.

```python
from collections import deque

q = deque([1, 2, 3])
q.append(4)             # right
q.appendleft(0)         # left
q.pop()                 # remove right
q.popleft()             # remove left
```

Gotchas:
- Random access is slower than list for deep indexing.
- Great for FIFO/LIFO ends, not for middle updates.

---

## 6) `heapq` (Priority Queue)

Python has a min-heap.

```python
import heapq

h = []
heapq.heappush(h, 5)
heapq.heappush(h, 2)
heapq.heappush(h, 9)
smallest = h[0]         # 2
x = heapq.heappop(h)    # 2
```

Max-heap pattern:

```python
vals = [5, 2, 9]
h = []
for v in vals:
    heapq.heappush(h, -v)
max_v = -heapq.heappop(h)
```

Tuple priority pattern:

```python
tasks = []
heapq.heappush(tasks, (2, "medium"))
heapq.heappush(tasks, (1, "urgent"))
# pops by first tuple element, then next element to break ties
```

Gotchas:
- `heapq` is not a sorted list; only `h[0]` is guaranteed smallest.
- Tie-breaking may fail for non-comparable payloads; include a monotonic counter when needed.

---

## 7) Dict Variants (`collections`)

### `defaultdict`
Avoid key-existence checks.

```python
from collections import defaultdict

freq = defaultdict(int)
for x in [1, 2, 2]:
    freq[x] += 1

groups = defaultdict(list)
for x in ["a", "ab", "b"]:
    groups[len(x)].append(x)
```

Gotcha:
- Reading `d[k]` creates the key if missing.

### `Counter`
Purpose-built frequency map.

```python
from collections import Counter

c = Counter("banana")
most_common = c.most_common(2)  # [('a', 3), ('n', 2)]
```

Gotcha:
- Counter allows zero/negative counts; call `+Counter()` or cleanup if needed.

### `OrderedDict`
Mostly historical since normal dict preserves insertion order.
Still useful for order-mutating APIs (`move_to_end`).

```python
from collections import OrderedDict

od = OrderedDict()
od["a"] = 1
od["b"] = 2
od.move_to_end("a")
```

### `ChainMap`
Combine multiple dicts without copying.

```python
from collections import ChainMap

defaults = {"timeout": 30, "retries": 2}
overrides = {"timeout": 10}
cfg = ChainMap(overrides, defaults)
cfg["timeout"]  # 10
cfg["retries"]  # 2
```

Gotcha:
- Writes go to first map only.

---

## 8) `queue` module structures (thread-safe)

Use for producer/consumer with threads.

```python
from queue import Queue, LifoQueue, PriorityQueue

q = Queue()
q.put("job")
job = q.get()
```

Variants:
- `Queue` -> FIFO
- `LifoQueue` -> stack
- `PriorityQueue` -> min-priority first

Gotcha:
- Slower than `deque` due to thread-safety overhead; use `deque` in single-threaded algorithms.

---

## 9) `array.array` (typed, compact numeric storage)

```python
from array import array

a = array('i', [1, 2, 3])
a.append(4)
```

Good when memory matters for homogeneous primitives.

---

## 10) Selection Cheatsheet

- Need index access / dynamic sequence: `list`
- Need FIFO queue / BFS: `deque`
- Need unique + fast membership: `set`
- Need key->value lookup/group/count: `dict` / `defaultdict` / `Counter`
- Need always get min/max efficiently: `heapq`

---

## 11) High-Value Gotchas

- Mutable default arguments:

```python
def f(x, acc=[]):   # bad
    acc.append(x)
    return acc
```

Use:

```python
def f(x, acc=None):
    if acc is None:
        acc = []
    acc.append(x)
    return acc
```

- Shallow vs deep copy:
  - `b = a[:]` or `a.copy()` is shallow.
  - Nested objects still shared.

- `is` vs `==`:
  - `is` compares identity.
  - `==` compares value.

- Hashability rule for keys/set elements:
  - Must be immutable/hashable (`int`, `str`, `tuple` with hashable elements, `frozenset`).
