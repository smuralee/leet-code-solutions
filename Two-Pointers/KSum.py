from typing import List
class Solution:
    def KSUM_two_pointers(self, nums: List[int], target: int, k:int) -> List[List[int]]:
        """KSUM main function 

        Args:
            nums (List[int]): _description_
            target (int): _description_
            k (int): _description_

        Returns:
            List[List[int]]: _description_
        """
	
        def kSum(nums: List[int], target: int, k: int) -> List[List[int]]:
            """ K Sum that calls Two Sum and iterate k-2 loops using recursion

            Args:
                nums (List[int]): List already sorted 
                target (int): _description_
                k (int): _description_

            Returns:
                List[List[int]]: _description_
            """
            res = []
            
            # If we have run out of numbers to add, return res.
            if not nums:
                print('Non element selected',k)
                return res
            
            # There are k remaining values to add to the sum. The 
            # average of these values is at least target // k.
            average_value = target // k
            
            # We cannot obtain a sum of target if the smallest value
            # in nums is greater than target // k or if the largest 
            # value in nums is smaller than target // k.
            if average_value < nums[0] or nums[-1] < average_value:
                print('invalid list provided',k)
                return res
            
            if k == 2:
                print(f"The sorted list is {nums} for {k}")
                return twoSum(nums, target)

            print(f"The sorted list is {nums} for {k}")
            for i in range(len(nums)):
                print(f"first number {i},{nums[i]},{k}")
                if i == 0 or nums[i - 1] != nums[i]:
                    for subset in kSum(nums[i + 1:], target - nums[i], k - 1):
                        print(nums[i], subset, k)
                        res.append([nums[i]] + subset)
            print(f'Return the result for {nums[i + 1:]}, {k}')
            return res

        def twoSum(nums: List[int], target: int) -> List[List[int]]:
            """Base case for recusion in KSum 

            Args:
                nums (List[int]): _description_
                target (int): _description_

            Returns:
                List[List[int]]: _description_
            """
            res = []
            lo, hi = 0, len(nums) - 1
    
            while (lo < hi):
                curr_sum = nums[lo] + nums[hi]
                if curr_sum < target or (lo > 0 and nums[lo] == nums[lo - 1]):
                    lo += 1
                elif curr_sum > target or (hi < len(nums) - 1 and nums[hi] == nums[hi + 1]):
                    hi -= 1
                else:
                    res.append([nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
            print(f'Result for TwoSum is {res}')                       
            return res

        nums.sort()
        print(nums)
        return kSum(nums, target, k)

    def KSUM_hash_map(self, nums:List[int], target:int, k:int):
            
        def KSum(nums:List[int], target:int, k:int):
            res = []

            if not nums: 
                return res 

            average_lower_bound = target//k
            if average_lower_bound < nums[0] or average_lower_bound > nums[-1]:
                return res 

            if k == 2: 
                return TwoSum(nums, target)

            else:

                for i in range(len(nums)): 
                    print(nums[i],k)
                    if i == 0 or nums[i] != nums[i-1]: 

                        for subset in KSum(nums[i+1:], target-nums[i], k-1): 
                            print(subset, nums[i])
                            res.append([nums[i]]+subset)
                            print(res)
                            print()
            return res 

        def TwoSum(nums:List[int], target:int) -> List[List[int]]: 
            
            res = []
            seen = set()
            for i in range(len(nums)): 
                if len(res) == 0 or res[-1][1] != nums[i]: 
                    if target-nums[i] in seen : 
                        res.append([target-nums[i],nums[i]])
                
                    seen.add(nums[i])
            #print(res)
            return res 

        nums.sort()
        print(nums)
        return KSum(nums, target, k)
        


if __name__ == "__main__":
    # nums = [1,0,-1,0,-2,2]
    # target = 0 
    # sol = Solution()
    # print(sol.KSUM_hash_map(nums,target,4))
    #print([nums+[target]])

    nums = [2,3,2,3]
    target = 5
    k = 2 

    sol = Solution()
    print(sol.KSUM_hash_map(nums,target,k))

    #print(sol.KSUM_two_pointers(nums,target,4))