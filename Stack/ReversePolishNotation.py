from typing import List 
from collections import deque
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:

        operator = set(['+','-','*','/'])

        queue = deque([])

        operator_count = 0 
        operant_count = 0

        def add(s1:str, s2:str)->int: 
            return int(s1) + int(s2)

        def minus(s1:str, s2:str)->int:
            return int(s1)-int(s2) 

        def times(s1:str, s2:str)-> int:
            return int(s1)*int(s2)

        def divide(s1:str, s2:str)-> int: 
            return int(int(s1))/(int(s2))

        operate_dic = {
            '+':add, 
            '-':minus,
            '/':divide,
            '*':times,
        }

        for token in tokens: 

            if token in operator: 
                operator_count += 1 
            else: 
                operant_count += 1 

            queue.append(token)

            if operant_count >= 2 and operator_count == 1: 

                queue.pop()
                re = operate_dic[token](queue[-1],queue[-2])
                queue.pop()
                queue.pop()
                queue.append(re)

                operant_count -= 2 
                operator_count = 0 

        return queue[0]
