def merge_sort(nums):
    n = len(nums)
    if n > 1:
        mid = n//2
        left = nums[:mid]
        right = nums[mid:]

        merge_sort(left)
        merge_sort(right)

        i, j , k = 0, 0, 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                nums[k] = left[i]
                i += 1
            else:
                nums[k] = right[j]
                j += 1
            k +=1

        while i < len(left):
            nums[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            nums[k] = right[j]
            j += 1
            k += 1

if __name__ == "__main__":
    data = [4, 3, 2, 1, 0, 8]
    merge_sort(data)
    print(data)
