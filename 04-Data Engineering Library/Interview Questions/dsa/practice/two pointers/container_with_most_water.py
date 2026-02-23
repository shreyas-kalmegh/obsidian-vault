class Solution:
    def maxArea(self, heights: List[int]) -> int:
        max_water = 0
        l, r = 0, len(heights) - 1 

        while l < r:
            total_water = (r - l) * min(heights[l], heights[r])
            max_water = max(max_water, total_water)

            if heights[l] >= heights[r]:
                r -= 1
            else: l +=1

        return max_water