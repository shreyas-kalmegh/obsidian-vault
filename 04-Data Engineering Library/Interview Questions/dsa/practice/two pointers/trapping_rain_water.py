def trap_rain_water(height):
    """
    Two-pointer solution.

    Time: O(n)
    Space: O(1)
    """
    n = len(height)
    if n < 3:
        return 0

    left = 0
    right = n - 1

    # Highest wall seen so far from each side.
    left_max = height[left]
    right_max = height[right]

    water = 0

    # Intuition:
    # Water above index i is limited by:
    # min(max wall on left of i, max wall on right of i) - height[i]
    #
    # We do not precompute arrays. Instead, we keep moving inward from both ends.
    # At each step, whichever side has the smaller current max is the "decidable" side:
    # - If left_max <= right_max, left side is limited by left_max for sure.
    #   (Right side has at least right_max, which is >= left_max.)
    # - Symmetrically, if right_max < left_max, right side is decidable.
    while left < right:
        if left_max <= right_max:
            left += 1
            left_max = max(left_max, height[left])
            # If current bar is below left_max, trapped water is the gap.
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            # If current bar is below right_max, trapped water is the gap.
            water += right_max - height[right]

    return water


if __name__ == "__main__":
    test_cases = [
        ([], 0),
        ([0], 0),
        ([0, 1, 0], 0),
        ([0, 1, 0, 2], 1),
        ([4, 2, 0, 3, 2, 5], 9),
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
    ]

    for arr, expected in test_cases:
        got = trap_rain_water(arr)
        assert got == expected, f"failed: input={arr}, got={got}, expected={expected}"

    print("all trapping rain water checks passed")
