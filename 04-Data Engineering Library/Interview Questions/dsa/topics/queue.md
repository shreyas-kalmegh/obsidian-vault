# Queue Fundamentals

## Why queue works
Queue = First-In, First-Out (FIFO).
Use it when processing order must follow arrival order.

## Core mental model
Queues model frontier expansion.
- Graph/tree BFS: nodes discovered first are processed first.
- Level-order tree traversal: each layer processed before next.

## Complexity
With `collections.deque`:
- `append`, `appendleft`, `popleft`, `pop` are `O(1)`.
- Do not use list `pop(0)` for queues (`O(n)`).

## High-value patterns

### BFS
- Initialize queue with start node.
- Mark visited at enqueue time (not dequeue time) to avoid duplicates.

### Sliding window deque
For max/min in window of size `k`.
- Maintain indices in monotonic order.
- Remove out-of-window indices from front.

## Common pitfalls
- Marking visited too late.
- Forgetting boundary checks in grid BFS.
- Mixing value and index in deque problems.

## Templates

### BFS on graph
```python
from collections import deque


def bfs(start, graph):
    q = deque([start])
    seen = {start}
    order = []

    while q:
        node = q.popleft()
        order.append(node)
        for nei in graph[node]:
            if nei not in seen:
                seen.add(nei)
                q.append(nei)
    return order
```

### Level-order tree traversal
```python
from collections import deque


def level_order(root):
    if not root:
        return []
    q = deque([root])
    ans = []

    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        ans.append(level)
    return ans
```
