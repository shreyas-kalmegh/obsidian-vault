def insertion_sort_for(nums):
    for i in range(1, len(nums)):
        curr = nums[i]
        insert_pos = 0

        # Find insertion position by scanning leftward.
        for j in range(i - 1, -1, -1):
            if nums[j] > curr:
                nums[j + 1] = nums[j]  # shift right
                insert_pos = j
            else:
                insert_pos = j + 1
                break

        nums[insert_pos] = curr

    return nums


def insertion_sort_while(nums):
    for i in range(1, len(nums)):
        curr = nums[i]
        j = i - 1

        while j >= 0 and nums[j] > curr:
            nums[j + 1] = nums[j]
            j -= 1

        nums[j + 1] = curr

    return nums

if __name__ == "__main__":
    data = [4, 3, 2, 1, 0, 8]
    print("for-loop version:", insertion_sort_for(data[:]))
    print("while-loop version:", insertion_sort_while(data[:]))
