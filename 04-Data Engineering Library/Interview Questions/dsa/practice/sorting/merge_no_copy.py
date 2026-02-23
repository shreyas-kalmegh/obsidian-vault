def merge_sort_in_place(nums):
    """
    In-place merge sort (no left/right copied sublists).
    Uses O(1) extra array space, but merge step can be slower due to shifting.
    """
    if len(nums) <= 1:
        return nums

    _merge_sort(nums, 0, len(nums) - 1)
    return nums


def _merge_sort(nums, left, right):
    if left >= right:
        return

    mid = (left + right) // 2
    _merge_sort(nums, left, mid)
    _merge_sort(nums, mid + 1, right)
    _merge_in_place(nums, left, mid, right)


def _merge_in_place(nums, left, mid, right):
    i = left
    j = mid + 1

    # Already sorted boundary; nothing to merge.
    if nums[mid] <= nums[j]:
        return

    while i <= mid and j <= right:
        if nums[i] <= nums[j]:
            i += 1
        else:
            # nums[j] belongs before nums[i].
            value = nums[j]
            k = j
            while k > i:
                nums[k] = nums[k - 1]
                k -= 1
            nums[i] = value

            # Window shifted by one after insertion.
            i += 1
            mid += 1
            j += 1


if __name__ == "__main__":
    data = [4, 3, 2, 1, 0, 8, 3, -1]
    print(merge_sort_in_place(data))
