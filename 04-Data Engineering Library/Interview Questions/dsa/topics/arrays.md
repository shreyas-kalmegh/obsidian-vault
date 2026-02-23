# Arrays Fundamentals

## What an array gives you
- Contiguous memory (conceptually): great for index-based access.
- `O(1)` read/write by index.
- Poor mid-array insertion/deletion (`O(n)` due to shifting).

## Core mental model
Think in terms of index ranges and invariants.
- Invariant example (two pointers): everything left of `l` is processed, everything right of `r` is processed.
- Invariant example (window): current window `[l, r]` satisfies a condition.

## Complexity cheat sheet
- Access by index: `O(1)`
- Linear scan: `O(n)`
- Sort first, then scan: `O(n log n)` + scan
- Prefix precompute + range query: build `O(n)`, query `O(1)`

## High-value patterns

### Two pointers
Use when array is sorted or when you compare from both ends.
- Typical signals: pair sum, palindrome-like checks, in-place partition.
- Common bug: moving both pointers without proving why.

### Sliding window
Use for contiguous subarray/substring optimization.
- Fixed window: size `k` known.
- Variable window: grow `r`, shrink `l` until condition holds.
- Common bug: forgetting to shrink in a `while` loop.

### Prefix sum
Use when many range-sum queries or counting subarray properties.
- Formula: sum of `[l..r] = pre[r+1] - pre[l]`.
- Common bug: off-by-one indexing.

## Interview checklist before coding
- Is order important?
- Is array sorted? If not, should I sort?
- Need contiguous segment or arbitrary picks?
- Can I trade space for time?

## Templates

### Two pointers (generic)
```python

def two_pointers(nums):
    l, r = 0, len(nums) - 1
    ans = None
    while l < r:
        if condition(nums[l], nums[r]):
            # update ans
            l += 1
        else:
            r -= 1
    return ans
```

### Sliding window (variable size)
```python

def longest_valid_window(nums):
    l = 0
    ans = 0
    state = {}  # counts/sum/etc

    for r, x in enumerate(nums):
        add_to_state(state, x)
        while not is_valid(state):
            remove_from_state(state, nums[l])
            l += 1
        ans = max(ans, r - l + 1)
    return ans
```

### Prefix sum
```python

def build_prefix(nums):
    pre = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        pre[i + 1] = pre[i] + x
    return pre


def range_sum(pre, l, r):
    return pre[r + 1] - pre[l]
```
