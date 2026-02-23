# Heap Fundamentals

## Why heap works
Heap gives fast access to min (or max) element.
- Min-heap root is smallest.
- Python `heapq` implements min-heap.

## Complexity
- Peek min: `O(1)`
- Push: `O(log n)`
- Pop min: `O(log n)`
- Build heap from list: `O(n)`

## Core mental model
Use heap when you repeatedly need the "best next" element under an ordering.
- Top-k elements
- Merge k sorted lists
- Scheduling by earliest time/priority

## High-value patterns

### Fixed-size heap for top-k
- Keep heap size `k`.
- If new candidate better than root, replace root.
- Total `O(n log k)`.

### Max-heap simulation in Python
- Push negative value: `heappush(h, -x)`.
- Pop and negate back.

### Two-heaps pattern (median)
- Max-heap for lower half, min-heap for upper half.
- Rebalance sizes to differ by at most one.

## Common pitfalls
- Forgetting `heapq` is min-heap.
- Popping all items when only k needed.
- Not rebalancing in two-heaps problems.

## Templates

### Top-k frequent elements
```python
import heapq
from collections import Counter


def top_k_frequent(nums, k):
    freq = Counter(nums)
    h = []
    for val, cnt in freq.items():
        heapq.heappush(h, (cnt, val))
        if len(h) > k:
            heapq.heappop(h)
    return [val for _, val in h]
```

### Kth largest in stream
```python
import heapq


class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.h = nums[:]
        heapq.heapify(self.h)
        while len(self.h) > k:
            heapq.heappop(self.h)

    def add(self, val):
        heapq.heappush(self.h, val)
        if len(self.h) > self.k:
            heapq.heappop(self.h)
        return self.h[0]
```
