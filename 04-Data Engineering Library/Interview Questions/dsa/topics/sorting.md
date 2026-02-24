# Sorting Notes (Interview Quick Reference)

## Intuition
Sorting pays an upfront cost so later logic becomes simpler.

After sorting, many problems become easy with:
- Two pointers
- Binary search
- Linear merge-style scans

Typical cost:
- Comparison sorts: `O(n log n)`

## When to Use
Use sorting when:
- You need order-based reasoning (min/max gaps, pairs, intervals).
- A brute-force pair search is `O(n^2)` and sorted two-pointer can reduce complexity.
- You need deterministic ordering before grouping/merging.

## Core Mental Model
Ask:
1. Should I sort first to simplify logic?
2. Do I need stable ordering?
3. Is in-place required, or can I use extra space?

## Complexity Snapshot
- Merge Sort: time `O(n log n)`, space `O(n)`, stable.
- Quick Sort: average `O(n log n)`, worst `O(n^2)`, usually in-place.
- Counting Sort: `O(n + k)` when values are bounded (`k` = range size).
- Python `sort()` / `sorted()`: `O(n log n)` worst-case, stable.

## Template 1: Merge Sort (Stable)
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    out = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1

    out.extend(left[i:])
    out.extend(right[j:])
    return out
```

## Template 2: Quick Sort (In-Place)
```python
def quick_sort(arr):
    def partition(l, r):
        pivot = arr[r]
        i = l
        for j in range(l, r):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[r] = arr[r], arr[i]
        return i

    def qs(l, r):
        if l >= r:
            return
        p = partition(l, r)
        qs(l, p - 1)
        qs(p + 1, r)

    qs(0, len(arr) - 1)
    return arr
```

## Template 3: Counting Sort (Non-Negative Ints)
```python
def counting_sort(nums):
    if not nums:
        return nums

    k = max(nums)
    count = [0] * (k + 1)

    for x in nums:
        count[x] += 1

    out = []
    for value, freq in enumerate(count):
        out.extend([value] * freq)

    return out
```

## Quick Example
`nums = [5, 2, 4, 2, 1]`
- Merge sort result: `[1, 2, 2, 4, 5]`
- Quick sort result: `[1, 2, 2, 4, 5]`
- Counting sort result: `[1, 2, 2, 4, 5]` (works since values are small non-negative ints)

## Common Pitfalls
- Ignoring quick sort worst-case with poor pivot choice.
- Using counting sort when value range is huge (memory blow-up).
- Forgetting whether stable sort is required.
- Sorting when you actually need original indices (store `(value, index)` if needed).

## Interview Tip
Default approach in Python interviews:
- Use built-in `sort()` unless interviewer asks for manual algorithm.
- Mention stability and complexity.
- Then solve the main problem using sorted structure (two pointers, merge intervals, etc.).
