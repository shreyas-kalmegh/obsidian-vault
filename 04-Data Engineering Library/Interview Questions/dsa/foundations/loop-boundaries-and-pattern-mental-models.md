# Loop Boundaries and Pattern Mental Models

Use this note when you feel stuck on loop bounds, loop direction, or pointer movement.

## Core Rule
Before writing a loop, answer 3 questions:
1. What region is already solved?
2. What region is still unknown?
3. After one iteration, what strictly shrinks the unknown region?

If you cannot answer these, your loop is likely wrong.

## Universal Boundary Checklist
- State valid index range first: usually `0..n-1`.
- Decide closed vs half-open intervals.
- Prefer half-open for clarity: `[start, end)`.
- Write loop invariant as a sentence.
- Run 3 dry runs mentally: empty input, single item, normal case.

## Loop Direction Mental Model

### Left to right (`i = 0 -> n-1`)
Use when current work depends on past elements only.
- Prefix sums
- Running counts
- Building answers incrementally

### Right to left (`i = n-1 -> 0`)
Use when current work depends on future elements only.
- Suffix arrays
- Next greater/smaller with stack (sometimes)
- Backward fill tasks

### Two pointers inward (`l++`, `r--`)
Use when you compare both ends or shrink a search space from both sides.
- Palindrome checks
- Pair sum in sorted array
- Partitioning tasks

## Pattern-by-Pattern Loop Templates

### 1) Fixed loop over array
Invariant: `0..i-1` processed.
```python
for i in range(n):
    # process nums[i]
```
Common mistakes:
- Using `range(n + 1)` accidentally
- Accessing `nums[i+1]` on last iteration

### 2) Adjacent comparison loop
Invariant: valid pair is `(i, i+1)`.
```python
for i in range(n - 1):
    if nums[i] > nums[i + 1]:
        ...
```
Common mistake:
- Forgetting `n - 1` and causing out-of-bounds at `i + 1`

### 3) Two pointers (sorted array)
Invariant: answer, if exists, is within `[l, r]`.
```python
l, r = 0, n - 1
while l < r:
    s = nums[l] + nums[r]
    if s == target:
        return [l, r]
    if s < target:
        l += 1
    else:
        r -= 1
```
Trick:
- Move exactly one pointer based on proof, not intuition.

### 4) Sliding window (variable size)
Invariant: window `[l, r]` is valid after shrink loop.
```python
l = 0
for r in range(n):
    add(nums[r])
    while not valid():
        remove(nums[l])
        l += 1
    # use window [l, r]
```
Trick:
- Use `while` to shrink, not `if`.

### 5) Binary search
Use half-open interval: `[lo, hi)`.
Invariant: answer lies inside `[lo, hi)`.
```python
lo, hi = 0, n
while lo < hi:
    mid = lo + (hi - lo) // 2
    if condition(mid):
        hi = mid
    else:
        lo = mid + 1
```
Trick:
- Choose one invariant style and never mix with closed interval style.

### 6) Reverse shift loop (insert into array)
Invariant: positions after `i` already shifted.
```python
for i in range(length, index, -1):
    arr[i] = arr[i - 1]
arr[index] = value
```
Trick:
- Shift right from end to start to avoid overwriting data.

### 7) Forward shift loop (remove from array)
Invariant: positions before `i` are compacted.
```python
for i in range(index, length - 1):
    arr[i] = arr[i + 1]
arr[length - 1] = None
length -= 1
```
Trick:
- Decrement length once after loop, not inside loop.

### 8) Nested loops in sorting
Outer loop decides sorted boundary.
Inner loop runs only in unsorted region.
Bubble sort idea:
```python
for i in range(n - 1):
    swapped = False
    for j in range(0, n - 1 - i):
        if nums[j] > nums[j + 1]:
            nums[j], nums[j + 1] = nums[j + 1], nums[j]
            swapped = True
    if not swapped:
        break
```
Trick:
- If inner loop does not shrink with `i`, you likely missed optimization or boundary logic.

## Fast Boundary Derivation Tricks
- If you read `i+1`, outer bound is usually `range(n - 1)`.
- If you read `i-1`, start from `1`.
- If you need both ends, initialize `l=0`, `r=n-1`, loop with `l < r`.
- If you need all windows of size `k`, start valid window when `r >= k - 1`.
- If you modify array in place:
  - shifting right -> iterate backward
  - shifting left -> iterate forward

## Off-by-One Debug Method (60 seconds)
1. Write expected valid indices.
2. Mark first iteration and last iteration values explicitly.
3. Check every indexed access at those two iterations.
4. Test on `[]`, `[x]`, and size 2.

## Problem-to-Pattern Detection Cues
- "contiguous", "longest substring/subarray" -> sliding window
- "sorted + pair" -> two pointers
- "search in monotonic answer space" -> binary search
- "next greater/smaller" -> monotonic stack
- "level by level" or minimum steps unweighted graph -> BFS queue

## Mini Practice Set for Boundaries
1. Reverse array in place (two pointers).
2. Remove duplicates from sorted array (slow/fast pointers).
3. Max sum subarray of size `k` (fixed window).
4. Smallest subarray with sum >= target (variable window).
5. First true in boolean monotonic array (binary search).
6. Insert at index in dynamic array (backward shift).
7. Remove at index in dynamic array (forward shift).
8. Bubble sort with early exit.

## Final Rule for Interviews
Speak invariant out loud before coding:
"At this point, everything before X is processed; I move Y so unknown region shrinks."
This single habit prevents most loop bugs.
