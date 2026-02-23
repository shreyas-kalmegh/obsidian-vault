def quick_sort(nums):
    """
    In-place quicksort using Lomuto partition.
    Returns the same list object after sorting.
    """
    if len(nums) <= 1:
        return nums

    _quick_sort(nums, 0, len(nums) - 1)
    return nums


def _quick_sort(nums, low, high):
    if low >= high:
        return

    pivot_index = _partition(nums, low, high)
    _quick_sort(nums, low, pivot_index - 1)
    _quick_sort(nums, pivot_index + 1, high)


def _partition(nums, low, high):
    # Pick the rightmost value as pivot.
    pivot = nums[high]
    i = low  # Next position for a value <= pivot.

    for j in range(low, high):
        if nums[j] <= pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1

    # Place pivot at its final sorted position.
    nums[i], nums[high] = nums[high], nums[i]
    return i


if __name__ == "__main__":
    data = [4, 3, 2, 1, 0, 8, 3, -1]
    print(quick_sort(data))
