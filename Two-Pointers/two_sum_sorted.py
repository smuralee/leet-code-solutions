from typing import List


class Solution(object):
    def twoSum_v1(self, numbers: List[int], target: int) -> List[int]:
        """
        :type numbers: List[int]
        :type target: int
        :rtype: List[int]

        O(N)
        """

        small_index = len(numbers) - 2
        large_index = len(numbers) - 1

        while numbers[small_index] + numbers[large_index] != target:

            # print(numbers[small_index], numbers[large_index])

            if numbers[small_index] + numbers[large_index] > target:
                small_index -= 1
                large_index -= 1

            else:
                large_index += 1

        return small_index + 1, large_index + 1

    def twoSum_v2(self, numbers: List[int], target: int) -> List[int]:
        """
        :type numbers: List[int]
        :type target: int
        :rtype: List[int]

        O(N)
        """

        small_index = 0
        large_index = len(numbers) - 1

        while numbers[small_index] + numbers[large_index] != target:

            if numbers[small_index] + numbers[large_index] > target:

                large_index -= 1

            else:
                small_index += 1

        return small_index + 1, large_index + 1


if __name__ == "__main__":
    sol = Solution()

    numbers_1 = [2, 7, 11, 15]
    target_1 = 9

    numbers_2 = [2, 3, 4]
    target_2 = 6

    numbers_3 = [-1, 0]
    target_3 = -1

    res1 = sol.twoSum_v2(numbers_1, target_1)
    print(res1)
    res2 = sol.twoSum_v2(numbers_2, target_2)
    print(res2)
    res3 = sol.twoSum_v2(numbers_3, target_3)
    print(res3)
