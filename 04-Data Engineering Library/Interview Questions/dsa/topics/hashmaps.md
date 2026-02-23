# HashMaps Fundamentals

## Why hash maps are powerful
- Average `O(1)` insert/lookup/delete.
- Convert repeated scanning (`O(n^2)`) to one pass (`O(n)`).

## Core mental model
A hash map stores derived state while scanning once.
Typical states:
- frequency of value
- first/last index of value
- complement needed to hit target
- grouping key -> list of elements

## Collision and worst-case note
- Interview complexity assumes average-case `O(1)` operations.
- Pathological worst-case can degrade, but usually not the focus.

## High-value patterns

### Counting
Used in anagrams, duplicates, top-k, majority style questions.

### Index map
Used in Two Sum, earliest occurrence, longest span tracking.

### Grouping
Canonical key -> bucket of items (e.g., group anagrams).

## Common pitfalls
- Forgetting to update map after using current element.
- Overwriting first index when you need earliest index.
- Mutating list/set while iterating incorrectly.

## Templates

### Counting pattern
```python
from collections import defaultdict


def count_values(nums):
    freq = defaultdict(int)
    for x in nums:
        freq[x] += 1
    return freq
```

### Two Sum pattern
```python

def two_sum(nums, target):
    idx = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in idx:
            return [idx[need], i]
        idx[x] = i
    return []
```

### Group by key
```python
from collections import defaultdict


def group_by_key(words):
    groups = defaultdict(list)
    for w in words:
        key = tuple(sorted(w))
        groups[key].append(w)
    return list(groups.values())
```
