def selection_sort(nums):
    n = len(nums)

    for i in range(n-1):
        max_pos = 0
        for j in range(n-i):
            if nums[j] > nums[max_pos]:
                max_pos = j
        nums[n-1-i], nums[max_pos] = nums[max_pos], nums[n-1-i]

    return nums

if __name__ == "__main__":
    test_cases = [
        ([], []),
        ([1], [1]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([4, 3, 2, 1], [1, 2, 3, 4]),
        ([3, 1, 3, 2], [1, 2, 3, 3]),
        ([4, 3, 2, 1, 0, 8], [0, 1, 2, 3, 4, 8]),
    ]

    for arr, expected in test_cases:
        result = selection_sort(arr[:])
        assert result == expected, f"failed: input={arr}, got={result}, expected={expected}"

    print("all selection sort checks passed")
