def two_sum_unsorted(nums: list[int], target: int) -> list[int]:
    """
    Time complexity: O(n)
    Space complexity: O(n)

    We loop through the list once, so O(n) time
    The map uses worst case O(n) space
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            # return the index of the num and complement
            return [seen[complement], i]
        else:
            # store the num in the map
            seen[num] = i
    return []
