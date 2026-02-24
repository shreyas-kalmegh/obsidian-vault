from collections import deque


def max_sliding_window(nums, k):
    """
    Return max value for every window of size k.

    Intuition:
    - Keep indices in a deque, values in decreasing order.
    - Front of deque is always the max for current window.
    """
    if not nums or k <= 0:
        return []

    q = deque()  # stores indices, nums[q[0]] is current window max
    result = []

    for r, value in enumerate(nums):
        # Remove indices that are out of this window [r-k+1, r].
        while q and q[0] <= r - k:
            q.popleft()

        # Maintain decreasing values in deque.
        # If current value is bigger, smaller ones behind it are useless.
        while q and nums[q[-1]] <= value:
            q.pop()

        q.append(r)

        # Start recording answers once first full window is formed.
        if r >= k - 1:
            result.append(nums[q[0]])

    return result


if __name__ == "__main__":
    test_cases = [
        (([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]),
        (([1], 1), [1]),
        (([9, 8, 7, 6], 2), [9, 8, 7]),
        (([4, 4, 4], 2), [4, 4]),
        (([], 3), []),
    ]

    for (nums, k), expected in test_cases:
        got = max_sliding_window(nums, k)
        assert got == expected, f"failed: nums={nums}, k={k}, got={got}, expected={expected}"

    print("all sliding window maximum checks passed")
