from typing import List 
import collections 

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:

        operator = set(['+','-','*','/'])

        queue = collections.deque([])

        operator_count = 0 
        operant_count = 0

        def add(s1:str, s2:str)->int: 
            return int(s1) + int(s2)

        def minus(s1:str, s2:str)->int:
            return int(s1)-int(s2) 

        def times(s1:str, s2:str)-> int:
            return int(s1)*int(s2)

        def divide(s1:str, s2:str)-> int: 
            
            return int(int(s1)/int(s2)) 

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
            #print(token, queue, operator_count, operant_count )

            if operant_count >= 2 and operator_count == 1: 

                queue.pop()
                #print(queue[-1], queue[-2])
                s1 = queue[-1]
                queue.pop()
                s2 = queue[-1]
                re = operate_dic[token](s2,s1)
                queue.pop()
                queue.append(re)

                operant_count -= 1
                operator_count = 0 

            #print(token, queue, operator_count, operant_count )
            #print()

        return queue[0]


if __name__ == '__main__':
    nums_1 = [100, 4, 200, 1, 3, 2]
    nums_2 = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
    nums_3 = [4, 0, -4, -2, 2, 5, 2, 0, -8, -8, -8, -8, -1, 7, 4, 5, 5, -4, 6, 6, -3]
    nums_4 = []
    nums_5 = [0]

    solution = Solution()

    print(solution.longestConsecutive(nums_1))
    print(solution.longestConsecutive(nums_2))
    print(solution.longestConsecutive(nums_3))
    print(solution.longestConsecutive(nums_4))
    print(solution.longestConsecutive(nums_5))
