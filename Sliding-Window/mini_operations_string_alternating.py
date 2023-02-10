class Solution(object):
    def minimumOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        max_even, max_odd = 0, 0 
        map_even, map_odd = {}, {}
        
        
        for i, j in zip(range(0,len(nums),2), range(1,len(nums),2)): 
            
            map_even[nums[i]] = map_even.get(nums[i], 0) + 1
            map_odd[nums[j]] = map_odd.get(nums[j], 0) + 1

            max_even = max(max_even, map_even.get(nums[i],0))
            max_odd = max(max_odd, map_odd.get(nums[j],0))
        
        # count_even_list = [[]] * count_even
        # count_odd_list = [[]] * count_odd 
        # for i, j in zip(range(0,len(nums),2), range(1,len(nums),2)): 
        #     count_even_list[map_even[nums[i]]].append(nums[i])

        # print(count_even_list)

        # print(len(nums),len(nums)%2)
        #print(max_even)
        #print(max_odd)
        
        # print(count_even)
        # print(count_odd)
        
        # print(len(map_even))
        # print(len(map_odd))

        return len(nums) - (max_even + max_odd)

if __name__ == '__main__': 

    sol = Solution()

    print(sol.minimumOperations(nums = [2,2,2,2]))