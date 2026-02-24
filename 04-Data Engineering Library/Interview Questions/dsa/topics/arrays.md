# Arrays Notes (Interview Quick Reference)

## Intuition
Arrays are index-based containers with fast random access.

Key tradeoff:
- Read/write by index is fast (`O(1)`)
- Middle insertion/deletion is expensive (`O(n)`) due to shifting

## When to Use
Array patterns dominate when problems ask about:
- Contiguous subarrays
- Pair relationships
- Running totals
- In-place transformations

## Core Mental Model
Track index boundaries and maintain an invariant.

Common invariants:
- Two pointers: everything before `l` and after `r` is already processed.
- Sliding window: current window `[l, r]` satisfies (or is being adjusted to satisfy) a condition.
- Prefix sum: `pre[i]` stores sum of first `i` elements.

## Complexity Cheat Sheet
- Access by index: `O(1)`
- Full scan: `O(n)`
- Sort + scan: `O(n log n)` + `O(n)`
- Prefix build: `O(n)`, range-sum query: `O(1)`

## Template 1: Two Pointers (Sorted Pair Sum)
```python
def pair_sum_sorted(nums, target):
    l, r = 0, len(nums) - 1

    while l < r:
        s = nums[l] + nums[r]
        if s == target:
            return [l, r]
        if s < target:
            l += 1
        else:
            r -= 1

    return [-1, -1]
```

## Template 2: Sliding Window (Variable Size)
```python
def longest_subarray_at_most_k_distinct(nums, k):
    from collections import defaultdict

    count = defaultdict(int)
    l = 0
    best = 0

    for r, x in enumerate(nums):
        count[x] += 1

        while len(count) > k:
            left_val = nums[l]
            count[left_val] -= 1
            if count[left_val] == 0:
                del count[left_val]
            l += 1

        best = max(best, r - l + 1)

    return best
```

## Template 3: Prefix Sum
```python
def build_prefix(nums):
    pre = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        pre[i + 1] = pre[i] + x
    return pre


def range_sum(pre, l, r):
    # sum of nums[l..r]
    return pre[r + 1] - pre[l]
```

## Quick Example
`nums = [1, 2, 3, 4, 5]`
- Prefix: `[0, 1, 3, 6, 10, 15]`
- Sum from index `1` to `3` is `pre[4] - pre[1] = 9`

## Common Pitfalls
- Off-by-one errors in loops and ranges.
- Forgetting to shrink window in a `while` loop.
- Moving both pointers without clear invariant.
- Mutating array while iterating in a way that breaks indices.

## Interview Tip
Before coding, classify the problem quickly:
- Contiguous segment -> sliding window or prefix sum.
- Pair in sorted data -> two pointers.
- Many range queries -> prefix sums.

This first classification usually determines the optimal pattern.
