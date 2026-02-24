# Hash Maps Notes (Interview Quick Reference)

## Intuition
A hash map is like a super-fast notebook:
- Key = what you look up
- Value = what you store about it

Instead of scanning the array again and again, you store useful info while traversing once.

Average-case operations:
- Insert: `O(1)`
- Lookup: `O(1)`
- Delete: `O(1)`

## When to Use
Use hash maps when you need:
- Fast membership checks (`x in seen`)
- Frequency counting
- Value -> index mapping
- Grouping by derived keys

## Core Mental Model
While scanning each element, ask:
1. What info do I need later?
2. What key represents that info?
3. Should I read from the map first, then write, or vice versa?

This read/write order is a common interview bug source.

## Template 1: Frequency Count
```python
from collections import defaultdict


def count_values(nums):
    freq = defaultdict(int)
    for x in nums:
        freq[x] += 1
    return freq
```

Quick example:
- Input: `[2, 2, 3, 1, 3, 3]`
- Output map: `{2: 2, 3: 3, 1: 1}`

## Template 2: Two Sum (Index Map)
```python
def two_sum(nums, target):
    idx = {}  # value -> index

    for i, x in enumerate(nums):
        need = target - x
        if need in idx:
            return [idx[need], i]
        idx[x] = i

    return []
```

Why read before write here:
- Prevent using the same element twice in one iteration.

Example:
- `nums = [2, 7, 11, 15], target = 9`
- Return `[0, 1]`

## Template 3: Group by Key (Group Anagrams Style)
```python
from collections import defaultdict


def group_anagrams(words):
    groups = defaultdict(list)

    for w in words:
        key = tuple(sorted(w))
        groups[key].append(w)

    return list(groups.values())
```

Alternative key for lowercase English letters:
- 26-length frequency tuple (often faster than sorting each word).

## Template 4: Longest Subarray with Given Sum (Prefix + Map)
```python
def longest_subarray_sum_k(nums, k):
    first_idx = {0: -1}  # prefix_sum -> earliest index
    prefix = 0
    best = 0

    for i, x in enumerate(nums):
        prefix += x

        if (prefix - k) in first_idx:
            best = max(best, i - first_idx[prefix - k])

        # keep earliest index only
        if prefix not in first_idx:
            first_idx[prefix] = i

    return best
```

## Common Pitfalls
- Overwriting earliest index when earliest is required.
- Updating map at wrong time (read vs write order bug).
- Assuming order in regular map iteration for logic that needs sorting.
- Using mutable objects as keys (invalid for Python dict keys).

## Complexity Notes
- Interview assumption: average `O(1)` for map ops.
- Pathological worst-case can degrade, but usually not the main focus.
- Space is typically `O(n)` in map-based one-pass solutions.

## Interview Tip
If a brute-force solution is `O(n^2)` because of repeated lookups, try:
- one pass
- hash map for state
- direct lookup in `O(1)` average

That often drops runtime to `O(n)`.
