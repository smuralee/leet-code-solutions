from typing import List 
from collections import deque
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # base cases
        n = len(nums)
        if n * k == 0:
            return []
        if k == 1:
            return nums
        
        def clean_deque(i):
            # remove indexes of elements not from sliding window
            print(deq)
            print()
            if deq and deq[0] == i - k:
                print(deq)
                deq.popleft()
                
            # remove from deq indexes of all elements 
            # which are smaller than current element nums[i]
            while deq and nums[i] > nums[deq[-1]]:
                deq.pop()
        
        # init deque and output
        deq = deque()
        max_idx = 0
        for i in range(k):
            print(deq)
            clean_deque(i)
            #print(deq)
            deq.append(i)
            print(f"After append {deq}")
            # compute max in nums[:k]
            if nums[i] > nums[max_idx]:
                max_idx = i
        output = [nums[max_idx]]
        
        # build output
        for i in range(k, n):
            clean_deque(i)          
            deq.append(i)
            output.append(nums[deq[0]])
        return output

if __name__ == '__main__': 

    sol = Solution()

    nums = [1,3,-1,-3,5,3,6,7]
    k = 3 

    output = sol.maxSlidingWindow(nums, k)

    '''
    IMPORTant feature about deque, empty deque will return Flase in the if statement 
    '''

    deq = deque()

    if deq: 

        print('DEQ')

    else: 
        print('NO DEQUE')

        