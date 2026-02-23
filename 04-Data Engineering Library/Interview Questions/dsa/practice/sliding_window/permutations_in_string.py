def contains_permutation(s1, s2):
    """
    Return True if any permutation of s1 appears as a substring of s2.

    Sliding window idea:
    - A permutation has the same character counts as s1.
    - So for every window of size len(s1) in s2, compare counts.
    """
    n1, n2 = len(s1), len(s2)
    if n1 > n2:
        return False

    need = {}
    window = {}

    for ch in s1:
        need[ch] = need.get(ch, 0) + 1

    # Build initial window of size n1.
    for i in range(n1):
        ch = s2[i]
        window[ch] = window.get(ch, 0) + 1

    if window == need:
        return True

    # Slide window one step at a time:
    # add right char, remove left char, then compare maps.
    left = 0
    for right in range(n1, n2):
        add_ch = s2[right]
        window[add_ch] = window.get(add_ch, 0) + 1

        remove_ch = s2[left]
        window[remove_ch] -= 1
        if window[remove_ch] == 0:
            del window[remove_ch]
        left += 1

        if window == need:
            return True

    return False


if __name__ == "__main__":
    test_cases = [
        ("ab", "eidbaooo", True),
        ("ab", "eidboaoo", False),
        ("adc", "dcda", True),
        ("hello", "ooolleoooleh", False),
        ("a", "a", True),
        ("abc", "bbbca", True),
    ]

    for s1, s2, expected in test_cases:
        result = contains_permutation(s1, s2)
        assert result == expected, (
            f"failed: s1={s1}, s2={s2}, got={result}, expected={expected}"
        )

    print("all permutation-in-string checks passed")
