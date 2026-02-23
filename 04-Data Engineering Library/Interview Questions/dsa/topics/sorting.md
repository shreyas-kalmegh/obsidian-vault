# Sorting Fundamentals

## First principles
Sorting is not just ordering; it enables faster downstream logic.
- After sorting, two pointers/binary search/interval merge become easy.
- Cost paid once (`O(n log n)`) can simplify the whole problem.

## Comparison vs non-comparison sorts
- Comparison-based lower bound: `O(n log n)` in general.
- Non-comparison (counting/radix/bucket) can be linear with strict constraints.

## Choosing the algorithm
- Need stable behavior and predictable runtime: merge sort.
- Need in-place average speed: quicksort.
- Values are small bounded integers: counting sort.
- Inputs distributed in buckets/ranges (often floats [0,1)): bucket sort.

## Stability and why it matters
A stable sort preserves relative order of equal keys.
- Important in multi-key sorting pipelines.
- Python built-in `sort()` is stable.

## Complexity snapshot
- Merge sort: `O(n log n)` time, `O(n)` extra space.
- Quicksort: average `O(n log n)`, worst `O(n^2)`, `O(log n)` stack average.
- Counting sort: `O(n + k)` time, `O(k)` space.
- Bucket sort: average near `O(n + k)` with good distribution.

## Common pitfalls
- Forgetting quicksort worst case with bad pivot choice.
- Using counting sort when range `k` is huge (memory blowup).
- Using bucket sort without checking data distribution assumptions.

## Templates

### Merge sort
```python

def merge_sort(a):
    if len(a) <= 1:
        return a
    m = len(a) // 2
    left = merge_sort(a[:m])
    right = merge_sort(a[m:])

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

### Quicksort (in-place)
```python

def quick_sort(a):
    def partition(l, r):
        pivot = a[r]
        i = l
        for j in range(l, r):
            if a[j] <= pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[r] = a[r], a[i]
        return i

    def qs(l, r):
        if l >= r:
            return
        p = partition(l, r)
        qs(l, p - 1)
        qs(p + 1, r)

    qs(0, len(a) - 1)
    return a
```

### Counting sort (non-negative ints)
```python

def counting_sort(nums):
    if not nums:
        return nums
    k = max(nums)
    cnt = [0] * (k + 1)
    for x in nums:
        cnt[x] += 1

    out = []
    for val, c in enumerate(cnt):
        out.extend([val] * c)
    return out
```

### Bucket sort (floats in [0, 1))
```python

def bucket_sort(nums):
    n = len(nums)
    buckets = [[] for _ in range(n)]
    for x in nums:
        idx = min(n - 1, int(x * n))
        buckets[idx].append(x)

    out = []
    for b in buckets:
        b.sort()
        out.extend(b)
    return out
```
