# Binary Search Notes (Interview Quick Reference)

## Intuition
Binary search works on **sorted** data.

Think of finding a word in a dictionary:
1. Open the middle.
2. If your word is smaller, search left half.
3. If bigger, search right half.
4. Repeat.

Each step removes half the remaining space.
- Time: `O(log n)`
- Space: `O(1)` (iterative)

## When to Use
Use binary search when:
- Data is sorted (or condition is monotonic: `False...False True...True`).
- You need fast lookup/index/position.

## Core Exact-Match Template
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

## First Occurrence (Leftmost Target)
Useful when duplicates exist.

```python
def first_occurrence(arr, target):
    left, right = 0, len(arr) - 1
    ans = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            ans = mid
            right = mid - 1  # continue left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return ans
```

## Lower Bound
First index `i` such that `arr[i] >= target`.
Returns `len(arr)` if no such index exists.

```python
def lower_bound(arr, target):
    left, right = 0, len(arr)  # search in [left, right)

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left
```

## Upper Bound
First index `i` such that `arr[i] > target`.
Returns `len(arr)` if no such index exists.

```python
def upper_bound(arr, target):
    left, right = 0, len(arr)  # search in [left, right)

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return left
```

## Find First and Last Position of Target
Classic interview problem.

```python
def search_range(arr, target):
    first = lower_bound(arr, target)

    # target not present
    if first == len(arr) or arr[first] != target:
        return [-1, -1]

    last = upper_bound(arr, target) - 1
    return [first, last]
```

## Quick Example
`arr = [1, 2, 2, 2, 4, 7]`, `target = 2`
- `first_occurrence(arr, 2) -> 1`
- `lower_bound(arr, 3) -> 4`
- `upper_bound(arr, 2) -> 4`
- `search_range(arr, 2) -> [1, 3]`

## Common Mistakes
- Using binary search on unsorted data.
- Infinite loops from incorrect boundary updates.
- Mixing closed interval `[l, r]` and half-open `[l, r)` logic.
- Mid overflow in some languages (`mid = l + (r-l)//2` is safer).

## Interview Tip
Decide interval style before coding:
- Exact match: usually closed interval `[left, right]`.
- Bounds (`lower/upper`): usually half-open `[left, right)`.

Being consistent with one style prevents most bugs.
