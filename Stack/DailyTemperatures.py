from collections import deque 
from typing import List 
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:

        """Solution using stack implemented by a deck 

        TC : O(N)
        SC : O(N)


        Returns:
            List[int]: List containing the 
        """

        res = [0]*len(temperatures)
        stack = deque()

        for i in range(len(temperatures)): 
         
            while stack and temperatures[i] > stack[-1][0]: 
                res[stack[-1][1]] += i-stack[-1][1]
                stack.pop()
            stack.append((temperatures[i],i))
            
        return res
            

if __name__ == "__main__": 

    temperatures = [71]*4
    #temperatures = [34,80,80,34,34,80,80,80,80,34]
    #temperatures = [30,40,50,60]
    #temperatures = [30, 60, 90]

    sol = Solution()

    print(sol.dailyTemperatures_idea1(temperatures))