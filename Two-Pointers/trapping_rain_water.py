from typing import List


class Solution(object):
    def trap(self, height: List[int]) -> int:
        """
        :type height: List[int]
        :rtype: int

        TC: O(N)
        SC: O(1)
        """

        ## find the left_start, max and right_start indedx 
        left_start = 0
        right_start = len(height) - 1
        max_height = 0
        max_i = 0

        ## collect the maximum value (O(N))
        for i in range(len(height)):
            if height[i] > max_height:
                max_height = height[i]
                max_i = i

                ## initialise the height of the rain catcher on two sides
        maxes = [height[left_start], height[right_start]]

        ## calculate the initial guess of the water trapped 
        # the first element is the amount of the water trapped from LHS
        # the second element is the amount of the water trapped from RHS
        resses = [
            height[left_start] * max((max_i - left_start - 1), 0),
            height[right_start] * max((right_start - max_i - 1), 0)
        ]

        ## intiliase the starting indixes to be one position after the 
        indexies = [left_start + 1, right_start - 1]

        ## start iterating left and right indexies and update the 
        # guess of the area 
        while indexies[0] < max_i or indexies[1] > max_i:
            # break when both the index is adjacent to the maximum index 
            for i, index in enumerate(indexies):

                if abs(max_i - index) > 0:

                    # setting this if loop for the case when we have 0 value to 
                    # start with on both sides 
                    if resses[i] != 0:
                        # update the reduction in the amount of the water trapped
                        resses[i] -= min(height[index], maxes[i])
                    #  update the increase in the amount of the water trapped
                    resses[i] += max(0, (height[index] - maxes[i])) * (abs(max_i - index) - 1)
                    # update the historical maximum rain catcher observed 
                    maxes[i] = max(height[index], maxes[i])
                    # move the indexies 
                    ## +1 if it's on the left 
                    ## -1 if it's on the right
                    indexies[i] += 1 if index < max_i else -1

        return sum(resses)

    def trap_submitted(self, height):
        """
        :type height: List[int]
        :rtype: int
        """

        #  find the left_start, max and right_start indedx
        left_start = 0
        right_start = len(height) - 1
        max_height = 0
        max_i = 0

        # collect the last occurence of the maximum value from the list 
        #  in the height list we can have multiple occurences of the
        #  maximum value
        for i in range(len(height)):
            if height[i] > max_height:
                max_height = height[i]
                max_i = i

        l_max = height[left_start]
        r_max = height[right_start]
        res_left = l_max * max((max_i - left_start - 1), 0)
        res_right = r_max * max((right_start - max_i - 1), 0)

        left_start += 1
        right_start -= 1

        while left_start < max_i or right_start > max_i:

            if max_i > left_start:

                height_to_deduct_left = min(height[left_start], l_max)
                height_to_add_left = max(0, (height[left_start] - l_max))

                if res_left != 0:
                    res_left -= height_to_deduct_left
                res_left += height_to_add_left * (max_i - left_start - 1)

                l_max = max(height[left_start], l_max)
                left_start += 1

            if max_i < right_start:

                height_to_deduct_right = min(height[right_start], r_max)
                height_to_add_right = max(0, (height[right_start] - r_max))

                if res_right != 0:
                    res_right -= height_to_deduct_right
                res_right += height_to_add_right * (right_start - max_i - 1)

                r_max = max(height[right_start], r_max)
                right_start -= 1

        return res_left + res_right


if __name__ == '__main__':
    height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    sol = Solution()
    res = sol.trap(height=height)
    print()
    print(res)

    height_1 = [4, 2, 0, 3, 2, 5]
    sol = Solution()
    res_1 = sol.trap(height=height_1)
    print()
    print(res_1)

    height_2 = [5, 4, 1, 2]
    sol = Solution()
    res_2 = sol.trap(height=height_2)
    print()
    print(res_2)
