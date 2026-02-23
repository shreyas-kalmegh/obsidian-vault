# Stack Fundamentals

## Why stack works
Stack = Last-In, First-Out (LIFO).
Use it when latest unresolved item must be processed first.

## Core mental model
Store unresolved state. When new data arrives, resolve as much as possible.
- Parentheses: unresolved opening brackets.
- Monotonic stack: unresolved indices waiting for next greater/smaller.

## Complexity
- Push/pop/top all `O(1)`.
- Each element is usually pushed once and popped once -> `O(n)` total.

## Monotonic stack intuition
Maintain increasing or decreasing order in stack.
- Next greater element: keep decreasing stack; pop while current is greater.
- Pop event is where answer gets assigned.

## Common pitfalls
- Storing values when you needed indices.
- Forgetting empty checks before `pop()`/`top`.
- Wrong comparison sign (`<` vs `<=`) causing duplicate-handling bugs.

## Templates

### Valid parentheses
```python

def is_valid_parentheses(s):
    pair = {')': '(', ']': '[', '}': '{'}
    st = []
    for ch in s:
        if ch in pair.values():
            st.append(ch)
        else:
            if not st or st[-1] != pair[ch]:
                return False
            st.pop()
    return not st
```

### Monotonic decreasing stack (next greater)
```python

def next_greater(nums):
    res = [-1] * len(nums)
    st = []  # indices, nums[st] strictly decreasing
    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            res[st.pop()] = x
        st.append(i)
    return res
```
