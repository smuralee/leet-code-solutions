from typing import List 
class permutation: 

    def generate(self,nums:List[int], start:int, end:int)-> List[List[int]]: 

        if (start == end):
            print (f"Termination condition {nums}")
        else:
            for i in range(start, end + 1):
                print(i, start)
                nums[start], nums[i] = nums[i], nums[start]  # The swapping
                print(f"prior {nums}")
                self.generate(nums, start + 1, end) 
                nums[start], nums[i] = nums[i], nums[start]  # Backtrackig
                print(i,start)
                print(f"posterior {nums}")

if __name__ == "__main__": 

    generator = permutation()

    generator.generate([1,2,3], 0, 2)