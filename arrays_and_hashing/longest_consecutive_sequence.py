from typing import List


def longest_consecutive_sequence(nums: List[int]) -> int:
    num_set = set(nums)
    longest = 0

    for n in nums:
        # check if it's the start of a sequence
        if (n - 1) not in num_set:
            length = 1
            while (n + length) in num_set:
                length += 1
            longest = max(length, longest)
    return longest


if __name__ == "__main__":
    nums_1 = [100, 4, 200, 1, 3, 2]
    nums_2 = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
    nums_3 = [4, 0, -4, -2, 2, 5, 2, 0, -8, -8, -8, -8, -1, 7, 4, 5, 5, -4, 6, 6, -3]
    nums_4 = []
    nums_5 = [0]

    print(longest_consecutive_sequence(nums_1))
    print(longest_consecutive_sequence(nums_2))
    print(longest_consecutive_sequence(nums_3))
    print(longest_consecutive_sequence(nums_4))
    print(longest_consecutive_sequence(nums_5))
