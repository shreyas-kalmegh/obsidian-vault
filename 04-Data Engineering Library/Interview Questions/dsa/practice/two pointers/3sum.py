class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        op = set()
        nums.sort()

        for i in range(len(nums)):
            j, k = i + 1, len(nums) - 1
            while j < k:
                total = nums[i] + nums[j] + nums[k]
                if total > 0:
                    k -= 1
                elif total < 0:
                    j += 1
                else:
                    op.add((nums[i], nums[j], nums[k]))
                    k -= 1
                    j += 1

        return [[i, j, k] for i, j, k in op]
# [-1,0,1,2,-1,-4]
# [-4, -1, -1, 0, 1, 2]