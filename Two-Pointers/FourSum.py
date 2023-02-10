from typing import List 
class Solution: 
    def fourSum_attempt_1_failed(self, nums: List[int], target: int)->List[List[int]]: 

        """
        Given an array of integers, return an array of all the unique quadruplets: [nums[a], nums[b], nums[c], nums[d]]
            such that a,b,c and d are distinct 
            AND
            nums[a] + nums[b] + nums[c] + nums[d] == target 
         
        Example: 

        Nums = [1,0,-1,0,-2,2], target = 0 

        A brute force method may go through N chooses 4 combinations, whihc is of time complexity N^4

        sorted Nums = [-2,-1,0,0,1,2] [Nlog(N)]

        [O(N^2)]
        L = -2, R = 2 terminsation condition: R_index - L_index < 2 
            largest sum = -2 + 2 + 0 + 1 
            smallest sum = -2 + 2 + -1 + 0
            -2 + 2 + -1 + 0 
            -2 + 2 + 0 + 0 
            -2 + 2 + 0 + 1 
            l = -1, r = 1 temination condition: r_index - l_index < 2 
            if sum == 0: 
                res.append(the selected tuple)
                move left up 
            if sum > 0 : 
                move right down 
            if sum < 0: 
                move left up 
        res = []
        defaultdict for storing the reult tuple, if inside the reuslt tuple, we don't appedn it to the result list 

        """
        nums.sort()
        print(nums)

        res = []
        visited = set()

        L = 0
        R = len(nums)-1

        while R-L > 2:
            
            t = target-(nums[R]+nums[L])

            l = L+1 
            r = R-1 

            while r-l>0: 
                combo = (nums[L], nums[l], nums[r], nums[R])
                print(combo,t)

                if combo not in visited:
                    visited.add((nums[L], nums[l], nums[r], nums[R]))

                    if nums[r]+nums[l]>t: 
                        r -=1 
                    elif nums[r]+nums[l]<t: 
                        l += 1 
                    else: 
                        res.append([nums[L], nums[l], nums[r], nums[R]])
                        l += 1 
                else: 
                    l += 1 
            
            if t < 0: 
                R-=1 
            elif t > 0: 
                L+= 1 
            else: 
                L+=1
                """

                This block, the edge case cannot be handled properly by the algorihtim, if the contribution from 
                the other two numbers are zero, moving in either directions could result in the fact that we miss 
                a valid combination 

                """

        return res 

    def fourSum(self, nums: List[int], target: int)->List[List[int]]: 
        """Four Sum optimal solution 

        Args:
            nums (List[int]): _description_
            target (int): _description_

        Returns:
            List[List[int]]: _description_

        As we csn only crack the Two Sum on a sorted array within O(N), 
        we create the condition for that to happen in 4 Sum. 

        sorted array 
        -3, -1, 0, 2, 4, 5 

        (-3,-1) (-3,0) ()

        """
        nums.sort()
        print(nums)

        res = []
        visited = set()

        for i in range(len(nums)-3):
            for j in range(i+1,len(nums)-2):
                #print(i,j)
                l, r = j+1, len(nums)-1
                #print(combo)
                while r-l>0:

                    if nums[l]+nums[r]+nums[i]+nums[j] > target: 
                        r -= 1 
                    elif nums[l]+nums[r]+nums[i]+nums[j] < target: 
                        l += 1
                    else: 
                        combo = (nums[i], nums[j],nums[l], nums[r])
                        if combo not in visited:
                            visited.add(combo)
                            res.append([nums[i], nums[j],nums[l], nums[r]])
                        l += 1 
                            
        return res 
            
if __name__ == "__main__": 

    nums = [1,0,-1,0,-2,2]
    target = 0 
    sol = Solution()
    print(sol.fourSum(nums,target))
    print()

    nums = [2,2,2,2,2]
    target = 8 
    sol = Solution()
    print(sol.fourSum(nums,target))
    print()


    nums = [-3,-1,0,2,4,5]
    target = 2 
    sol = Solution()
    print(sol.fourSum(nums,target))
    print()


    nums = [-3,-2,-1,0,0,1,2,3]
    target = 0 
    sol = Solution()
    print(sol.fourSum(nums,target))
    print()
