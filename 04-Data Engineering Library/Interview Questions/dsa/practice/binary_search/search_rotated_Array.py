class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left , right = 0, len(nums) - 1

        while left < right:
            mid = left + (right - left) // 2

            if nums[mid] < nums[right]:
                right = mid
            else:
                left = mid + 1
        
        pivot = left

        def binary_search(left, right):
            while left <= right:
                mid = left + (right - left) // 2
                if nums[mid] == target:
                    return mid
                if target > nums[mid]:
                    left = mid + 1
                else:
                    right = mid - 1
            return -1

        op = binary_search(0, pivot - 1)
        if op == -1:
            op = binary_search(pivot, len(nums) - 1)

        return op    