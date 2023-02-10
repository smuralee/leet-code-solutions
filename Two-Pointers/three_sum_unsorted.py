class Solution(object):

    def binary_search(target, nums):
        li = 0
        ri = len(nums) - 1
        FOUND = False
        print(nums, target)
        while li <= ri:

            ti = (li + ri) // 2
            if nums[ti] > target:
                ri = ti - 1
            elif nums[ti] < target:
                li = ti + 1
            else:
                FOUND = True
                return nums[ti], FOUND
            # print(li, ri, ti)
        return nums[ti], FOUND

    def ThreeSum(self, nums):

        """
        Attempt to write algo in Nlog(N), 
        failed version, will not pass all test cases
        """

        nums.sort()
        print(nums)
        #  O(nlog(n))

        res = [[]]
        left_index = 0
        right_index = len(nums) - 1

        while left_index < right_index:

            print(left_index, right_index)
            #  O(N)
            target = 0 - (nums[left_index] + nums[right_index])

            # print(nums[left_index], nums[right_index], target)

            if target < nums[left_index]:
                right_index -= 1

            elif target > nums[right_index]:
                left_index += 1

            else:
                #  conduct a binary search on the rest (Olog(N))
                temp_nums = nums[:left_index] + nums[left_index + 1:right_index] + nums[right_index + 1:]

                num, FOUND = Solution.binary_search(target, temp_nums)
                print(num, FOUND)
                # adding to the res list 
                if FOUND:
                    temp_list = [
                        nums[left_index],
                        nums[right_index],
                        num,
                    ]
                    if temp_list != res[-1]:
                        res.append(temp_list)

                    left_index += 1
                    right_index -= 1

                    # if num > 0: 
                    #     left_index += 1 

                    # elif num == 0: 
                    #     left_index += 1
                    #     right_index -=1 
                    # else: 
                    #     right_index -=1 

                else:

                    if num > target:
                        right_index -= 1

                    else:
                        left_index += 1

        return res[1:]

    def threeSum(slef, nums):

        """
        O(n**2) complexity
        """

        res = [[]]

        nums.sort()
        #  N(log(N)

        for i in range(len(nums) - 1):
            #  N
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            if nums[i] > 0:
                return res[1:]
            else:
                point = nums[i]
                l = i + 1
                r = len(nums) - 1

                while l < r:

                    if point + nums[l] + nums[r] == 0:

                        if [nums[l], point, nums[r]] != res[-1]:
                            res.append([nums[l], point, nums[r]])

                        l += 1
                        r -= 1

                    elif point + nums[l] + nums[r] < 0:

                        l += 1

                    else:
                        r -= 1

        return res[1:]

    def ThreeSum_hashset(self, nums, target): 
        


if __name__ == "__main__":
    nums_1 = [-1, 0, 1, 2, -1, -4]
    nums_2 = [-2, 0, 1, 3]
    nums_3 = [-1, 0, 1, 0]
    nums_4 = [-2, 0, 1, 1, 2]
    nums_5 = [-2, 0, 0, 2, 2]

    sol = Solution()

    res = sol.threeSum(nums_1)
    print()
    print(res)
    print()

    res_2 = sol.threeSum(nums_2)
    print()
    print(res_2)
    print()

    res_3 = sol.threeSum(nums_3)
    print()
    print(res_3)
    print()

    res_4 = sol.threeSum(nums_4)
    print()
    print(res_4)
    print()

    res_5 = sol.threeSum(nums_5)
    print()
    print(res_5)
    print()
    # print(sol.ThreeSum(nums_3))
    # print(sol.ThreeSum(nums_4))
