import collections
from typing import List 
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:

        res_l = 0
        i_l = 0
        stack = collections.deque([])

        for i in range(len(heights)): 
            while stack and heights[i] < stack[-1][0]: 
                if stack[-1][0]*(i-stack[-1][1]) > res_l:
                    res_l = stack[-1][0]*(i-stack[-1][1])
                    i_l = i
                stack.pop()
            stack.append((heights[i],i))
        print(stack, res_l)
        print()
        # cleareance 
        while stack: 
            if stack[-1][0]*(len(heights)-stack[-1][1]) > res_l:
                res_l = stack[-1][0]*(len(heights)-stack[-1][1])
                i_l = stack[-1][1]
            stack.pop()
            print(stack, res_l)


        res_r = 0 
        i_r = len(heights)-1
        stack = collections.deque([])

        for i in range(len(heights)-1, -1, -1): 
            while stack and heights[i] < stack[-1][0]: 
                if stack[-1][0]*(stack[-1][1]-i) > res_r:
                    res_r = stack[-1][0]*(stack[-1][1]-i)
                    i_r = i
                stack.pop()
            stack.append((heights[i],i))
        
        print(stack, res_r,)
        print()
        # clearance
        while stack: 
            if stack[-1][0]*(stack[-1][1]+1) > res_r:
                res_r = stack[-1][0]*(stack[-1][1]+1)
                i_r = stack[-1][1]
            stack.pop()
            print(stack, res_r)
        
        if i_l != i_r:
            return max(res_l, res_r)
        else: 
            return res_l + res_r - heights[i_l]

if __name__ == '__main__': 

    h = [2,1,2]
    sol = Solution()
    print(sol.largestRectangleArea(heights=h))
