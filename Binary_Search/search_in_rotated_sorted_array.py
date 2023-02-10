from typing import List
class Solution: 

    def search(self, nums:List[int], target: int) -> int: 

        # find the seperation point 
        l = 0 
        r = len(nums)-1 
        sep = r
        while l <= r: 
            
            mid = (l+r)//2 
            if nums[mid] > nums[-1]: 
                l = mid+1 
            else: 
                sep = min(sep,mid)
                r = mid-1 

        # search through the first array 
        def b_search(l:int, r:int, lis:List[int], target:int, last_one:bool = False) -> int: 

            while l <= r:
                mid = (l+r)//2 
                if lis[mid] < target: 
                    l = mid + 1 
                elif lis[mid] > target: 
                    r = mid - 1 
                else: 
                    if last_one: 
                        return mid+sep 
                    else: 
                        return mid
            return -1 

        inputs = [(0, sep-1, nums[:sep], target, False), (0, len(nums[sep:])-1, nums[sep:], target, True),]
        for i in inputs:
            res = b_search(i[0],i[1],i[2],i[3],i[4])

        return res


if __name__ == "__main__": 

    sol = Solution()
    print(sol.search(
        nums = [4,5,6,7,0,1,2],
        target=0
    ))
        
