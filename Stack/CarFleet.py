from collections import Counter
from typing import List 
class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int: 

        res = len(position)

        if res == 1: 
            return res 

        else: 
            pos_speed = sorted(
                zip(position,speed),key = lambda x:x[0], reverse=True,
            )


            def recursive(pos_speed, res):
                print(pos_speed)
                if len(pos_speed)>1:
                    stack = [] 
                    for pos, speed, in pos_speed: 

                        if pos >= target: 
                            continue

                        new_pos = pos + speed 

                        while stack and new_pos >= stack[-1][0]: 

                            new_pos = min(new_pos, stack[-1][0])
                            speed = min(speed, stack[-1][1])

                            stack.pop()
                            res -= 1 
                    
                        stack.append((new_pos, speed))

                    return recursive(stack, res)
                else:
                    return res 

            res = recursive(pos_speed, res)

            return res 
            
if __name__ == '__main__':

    sol = Solution()

    position = [8,3,7,4,6,5]
    speed = [4,4,4,4,4,4]
    target = 10

    print(sol.carFleet(target, position, speed))
