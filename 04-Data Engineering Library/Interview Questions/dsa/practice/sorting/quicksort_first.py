def quicksort(nums):
    return _quicksort(nums, 0, len(nums) - 1)


def _quicksort(nums, left, right):
    if left < right:
        splitpoint = _partition(nums, left, right)
        _quicksort(nums, left, splitpoint - 1)
        _quicksort(nums, splitpoint + 1, right)

    return nums

def _partition(nums, left, right):
    pivot = left
    leftmark = left + 1
    rightmark = right
    done = False

    while not done:
        while leftmark <= rightmark and nums[leftmark] <= nums[pivot]:
            leftmark += 1

        while rightmark >= leftmark and nums[rightmark] >= nums[pivot]:
            rightmark -= 1
        
        if rightmark < leftmark:
            done = True
        else:
            nums[leftmark], nums[rightmark] = nums[rightmark], nums[leftmark]

    nums[pivot], nums[rightmark] = nums[rightmark], nums[pivot]

    return rightmark
    
if __name__ == "__main__":
    data = [4, 3, 2, 1, 0, 8, 3, -1]
    print(quicksort(data))