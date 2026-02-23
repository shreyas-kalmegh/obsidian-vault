class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        # Notes on why this approach is incorrect:
        # 1) Wrong condition:
        #    You used len(subset) <= k + 1 (unique chars in window).
        #    But this problem is about replacements needed, not unique count.
        #    Correct validity rule is:
        #    window_len - frequency_of_most_common_char <= k
        #
        # 2) Using a set loses frequency information:
        #    set only tracks existence, not how many times a char appears.
        #    We need counts to know how many replacements are required.
        #
        # 3) Removing from set is unsafe with duplicates:
        #    subset.remove(s[l]) may remove a char that still exists in window.
        #    That makes window state incorrect.
        #
        # 4) Left pointer is never advanced in shrink loop:
        #    In while len(subset) > k + 1, l must be incremented.
        #    Without l += 1, logic can get stuck / drift.
        #
        # 5) cal is not guaranteed to equal current window length:
        #    Because window updates and removals are not synchronized correctly.
        subset = set()
        l = 0
        max_length = 0
        cal = 0

        for r in range(len(s)):
            while len(subset) > k + 1:
                subset.remove(s[l])
                cal -= 1
            subset.add(s[r])
            cal += 1
            if len(subset) <= k + 1:
                max_length = max(max_length, cal)
            
        return max_length

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        # Why this one works:
        # - Fix a target char c and ask:
        #   "What is the longest window that can be turned into all c
        #    using at most k replacements?"
        # - In a window [l..r], replacements needed =
        #   window_len - count_of_c_in_window
        # - If that is > k, shrink from left until valid.
        #
        # This is correct because it directly enforces the real invariant:
        # replacements needed <= k.
        #
        # Complexity:
        # - Let U = number of unique chars.
        # - Time: O(U * n), Space: O(1) or O(U) depending on alphabet model.
        #
        # How to improve further:
        # - Use one sliding window with a frequency map + max_freq tracker
        #   to get O(n) time overall.
        res = 0
        charSet = set(s)

        for c in charSet:
            count = l = 0
            for r in range(len(s)):
                if s[r] == c:
                    count += 1

                while (r - l + 1) - count > k:
                    if s[l] == c:
                        count -= 1
                    l += 1

                res = max(res, r - l + 1)
        return res


class SolutionLinear:
    def characterReplacement(self, s: str, k: int) -> int:
        # O(n) sliding window:
        # Keep frequency of chars in current window and track max_freq (highest count
        # of any single char in the window). Replacements needed is:
        # window_len - max_freq
        # If replacements needed > k, shrink from left.
        freq = {}
        l = 0
        max_freq = 0
        best = 0

        for r, ch in enumerate(s):
            freq[ch] = freq.get(ch, 0) + 1
            max_freq = max(max_freq, freq[ch])

            while (r - l + 1) - max_freq > k:
                left_ch = s[l]
                freq[left_ch] -= 1
                l += 1

            best = max(best, r - l + 1)

        return best
