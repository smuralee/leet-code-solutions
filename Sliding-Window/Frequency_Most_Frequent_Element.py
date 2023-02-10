class Solution(object):
    def maxFrequency(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        i, j = 0, 0
        sum_num = 0

        res = 0

        nums.sort()

        while j < len(nums):
            sum_num += nums[j]

            while sum_num + k < nums[j] * (j - i + 1):
                sum_num -= nums[i]
                i += 1

            res = max(res, (j - i + 1))
            j += 1

        return res

