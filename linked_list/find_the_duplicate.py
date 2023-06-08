from typing import List


class Solution:

    """This is a very good question for practiceing multiple solutions
    to solve one question, we will elaborate
    """

    def findDuplicate(self, nums: List[int]) -> int:
        """Binary search solution
        TC: O(Nlog(N))
        SC: O(1), discount the input

        Args:
            nums (List[int]): _description_

        Returns:
            int: _description_
        """

        nums = sorted(nums)
        l = 0
        r = len(nums) - 1

        while r - l > 1:
            mid = (l + r) // 2

            r_diff = nums[r] - nums[mid]
            l_diff = nums[mid] - nums[l]

            if r_diff == r - mid:
                r = mid

            elif r_diff > r - mid:
                r = mid

            else:
                l = mid

        return nums[l]

    def findDuplicate_floyd(self, nums: List[int]) -> int:
        """
        TC: O(N)
        SC: O(1)

        Returns:
            _type_: _description_
        """

        slow, fast = 0, 0

        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]

            if slow == fast:
                break

        slow_2 = 0
        while slow_2 != slow:
            slow_2 = nums[slow_2]
            slow = nums[slow]

        return slow
