class Solution:
    def minWindow(self, s: str, t: str) -> str:
        count_w = {}
        count_t = {}
        res = [-1, -1]
        reslen = float("infinity")
        have, need = 0, len(count_t)
        l = 0

        for c in t:
            count_t[c] = count_t.get(c, 0) + 1

        for r in range(len(s)):
            ch = s[r]
            count_w[ch] = count_w.get(ch, 0) + 1

            if ch in count_t and count_w[ch] == count_t[ch]:
                have += 1

            while have == need:
                wlen = r - l + 1
                if wlen < reslen:
                    reslen = wlen
                    res = [l, r]
                
                count_w[s[l]] -= 1
                if s[l] in count_t and count_w[s[l]] < count_t[s[l]]:
                    have -= 1
                l += 1


        return s[res[0] : res[1] +  1] if reslen != float("infinity") else ""