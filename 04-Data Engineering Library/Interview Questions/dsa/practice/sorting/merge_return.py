def merge_sort(nums):
    # Base case: lists of size 0 or 1 are already sorted.
    n = len(nums)
    if n > 1:
        # 1) Divide the input into two halves.
        mid = n // 2
        left = nums[:mid]
        right = nums[mid:]

        # 2) Recursively sort each half.
        left = merge_sort(left)
        right = merge_sort(right)

        # 3) Merge sorted halves back into nums.
        # i -> index for left, j -> index for right, k -> write index for nums.
        i, j, k = 0, 0, 0

        # Pick the smaller front element from left/right and write it into nums.
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                nums[k] = left[i]
                i += 1
            else:
                nums[k] = right[j]
                j += 1
            k += 1

        # Copy any remaining items from left.
        while i < len(left):
            nums[k] = left[i]
            i += 1
            k += 1

        # Copy any remaining items from right.
        while j < len(right):
            nums[k] = right[j]
            j += 1
            k += 1

    # Returns the same list object, now sorted in ascending order.
    return nums

if __name__ == "__main__":
    data = [4, 3, 2, 1, 0, 8]
    print(merge_sort(data))
