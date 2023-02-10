from typing import List
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:

        flatten_list = matrix[0]

        for row in matrix[1:]: 
            flatten_list += row

        l = 0 
        r = len(flatten_list)-1 

        while l <= r: 
            mid = (l+r)//2 
            print(mid)
            if flatten_list[mid] < target: 
                l = mid
            elif flatten_list[mid] > target: 
                r = mid 
            else: 
                return True 

        return False

if __name__ == '__main__': 

    matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
    target = 3

    matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
    target = 13 
    sol = Solution()
    print(sol.searchMatrix(matrix, target))