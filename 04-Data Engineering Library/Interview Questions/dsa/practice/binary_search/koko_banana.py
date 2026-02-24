# Koko Eating Bananas
# Medium Topics Company Tags
# Hints

# You are given an integer array piles where piles[i] is the number of bananas in the ith pile. You are also given an integer h, which represents the number of hours you have to eat all the bananas.

# You may decide your bananas-per-hour eating rate of k. Each hour, you may choose a pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, you may finish eating the pile but you can not eat from another pile in the same hour.

# Return the minimum integer k such that you can eat all the bananas within h hours.

# Example 1:

# Input: piles = [1,4,3,2], h = 9

# Output: 2

# Explanation: With an eating rate of 2, you can eat the bananas in 6 hours. With an eating rate of 1, you would need 10 hours to eat all the bananas (which exceeds h=9), thus the minimum eating rate is 2.

from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        left, right = 1, max(piles)
        res = h
        def calculate_hrs(speed: int) -> int:
            total = 0
            for pile in piles:
                # can use math.ceil(pile/speed)
                total += (pile + speed - 1) // speed
            return total

        while left <= right:
            mid = left + (right - left) // 2
            total_hrs = calculate_hrs(mid)

            if total_hrs <= h:
                res = mid
                right = mid - 1
            else:
                left = mid + 1

        return mid


if __name__ == "__main__":
    solver = Solution()
    tests = [
        # (piles, h, expected_min_speed)
        ([1, 4, 3, 2], 9, 2),
        ([3, 6, 7, 11], 8, 4),
        ([30, 11, 23, 4, 20], 5, 30),
        ([30, 11, 23, 4, 20], 6, 23),
    ]

    for piles, h, expected in tests:
        got = solver.minEatingSpeed(piles, h)
        status = "PASS" if got == expected else "FAIL"
        print(
            f"{status}: piles={piles}, h={h}, expected={expected}, got={got}"
        )
