def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    """
    Time complexity: O(n)
    Space complexity: O(1)

    Moving left to right can only increase the sum.
    Moving right to left can only decrease the sum.
    Sorted order guarantees this, which is why two pointers doesn't work on unsorted arrays.

    We do one pass, through the list, O(n)
    We don't need more space for storage, O(1)
    """
    left, right = (0, len(nums) - 1)
    while left < right:
        curr_sum = nums[left] + nums[right]
        if curr_sum == target:
            return [left + 1, right + 1]
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]
