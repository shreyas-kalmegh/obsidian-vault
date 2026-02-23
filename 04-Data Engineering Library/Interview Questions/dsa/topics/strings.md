# Strings Fundamentals

## What is special about strings
- Strings are usually immutable in interviews/languages like Python.
- Random access is `O(1)`, but repeated concatenation can be expensive.
- Treat strings as arrays of characters for most techniques.

## Core mental model
Most string problems are either:
- frequency/state tracking problems, or
- window boundary problems.

## High-value patterns

### Frequency map
Use when matching/anagram/permutation constraints appear.
- Track counts with hash map.
- Compare maps exactly or via a running "matches" counter.

### Two pointers on string
Use for palindrome, compression, or trim/clean tasks.
- Left and right pointers move based on rule.
- Common bug: mishandling non-alphanumeric characters.

### Sliding window on string
Use for longest/shortest substring with constraint.
- Maintain char counts in window.
- Expand right, shrink left until valid.

## Complexity decisions
- Brute force substrings can be `O(n^2)` or worse.
- Sliding window typically gives `O(n)`.
- Map/set space usually `O(k)` where `k` is charset size in window.

## Interview checklist before coding
- Is it contiguous substring or subsequence?
- Case sensitive?
- Ignore symbols/spaces?
- Fixed alphabet (e.g., lowercase) or full Unicode?

## Templates

### Character frequency
```python
from collections import Counter


def char_freq(s):
    return Counter(s)
```

### Longest substring without repeating characters
```python

def length_of_longest_unique_substring(s):
    seen = {}
    l = 0
    ans = 0

    for r, ch in enumerate(s):
        if ch in seen and seen[ch] >= l:
            l = seen[ch] + 1
        seen[ch] = r
        ans = max(ans, r - l + 1)
    return ans
```

### Palindrome check with filtering
```python

def is_palindrome_alnum(s):
    l, r = 0, len(s) - 1
    while l < r:
        while l < r and not s[l].isalnum():
            l += 1
        while l < r and not s[r].isalnum():
            r -= 1
        if s[l].lower() != s[r].lower():
            return False
        l += 1
        r -= 1
    return True
```
