from typing import List


def binary_search_sorted(nums: List[int], target):
    left_index = 0
    right_index = len(nums) - 1

    target_index = (left_index + right_index) // 2

    while nums[target_index] != target:

        # print(nums[target_index])

        if nums[target_index] > target:

            right_index = target_index

        else:

            left_index = target_index

        target_index = (left_index + right_index) // 2

    print(nums[target_index])

    return target_index


if __name__ == '__main__':
    nums = [-5, -6, -6, -3, -1, 0, 3, 5, 9, 12, 100]

    print(binary_search_sorted(nums, -1))
