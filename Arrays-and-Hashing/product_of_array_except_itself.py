from typing import List


def productExceptSelf(nums: List[int]) -> List[int]:
    """
    :type nums: List[int]
    :rtype: List[int]
    :solution must be provided without using divsion method 

    Solution: 
    - Initialise the array as all elements equal to 1, product default to 1, subject to modifications 
    - Go through the entire array from left hand side to right hand side 
       - (Note here we omit the first element when we start from left, as nothing is on its left) 
       - left hand side product = left hand side product from previous position * the value of the previous position 


    - Initilasie a number to keep track of the accumulative product on the RHS 
    - Go thoguh the entire array from right hand side to left hand sde 
       - (Note here we omit the first element when we start from right, as nothing is on its right) 
       -  update the result array, such that 
        - final result = left hand side product (re[i]) * accumulative product from right 
        - increase the accumulative product value as we iterate through 

    Complexity: 
    - N = len(nums)
    - TC: 0(N-1) ~ O(N)
    - SC: 0(N) 
          OR 0(1) if discount the storage for the output array 
    """
    res = [1] * len(nums)

    #  left propogation
    for i in range(1, len(nums)):
        res[i] = res[i - 1] * nums[i - 1]

    # right propogation 
    right_prod = nums[-1]
    for i in range(len(nums) - 2, -1, -1):
        res[i] *= right_prod
        right_prod *= nums[i]

    return res


if __name__ == '__main__':
    nums_1 = [1, 2, 3, 4]
    nums_2 = [-1, 1, 0, -3, 3]

    print(productExceptSelf(nums_1))
    print(productExceptSelf(nums_2))
