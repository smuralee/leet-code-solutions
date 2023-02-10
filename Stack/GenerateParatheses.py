from typing import List 
from collections import deque
class Solution:
    def generateParenthesis(self, n: int) -> List[str]: 

        """
        When we try to generate Parenthesis, 

            - we stop to generate parenthesis if Nopen == Nclose = n 
            - we may add a close parenthesis if Nclose < Nopen, otherwise we can only append a open parenthesis 
        """

        stack = []
        res = []

        def backtrack(Nopen:int, Nclose:int): 

            if Nopen == n and Nclose == n: 
                res.append("".join(stack))
                return 

            if Nopen < n: 
                if Nopen > Nclose: 

                    stack.append(')')
                    backtrack(Nopen, Nclose+1)
                    stack.pop()

                    stack.append('(')
                    backtrack(Nopen+1, Nclose)
                    stack.pop()

                else: 
                    stack.append('(')
                    backtrack(Nopen+1, Nclose)
                    stack.pop()
            else: 
                stack.append(')')
                backtrack(Nopen, Nclose+1)
                stack.pop()

        backtrack(0,0)
        return res 




if __name__ == '__main__': 


    sol = Solution()
    print(sol.generateParenthesis(3))