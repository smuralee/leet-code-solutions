from turtle import right
from black import diff
from soupsieve import match


class Solution(object):
    def findClosestElements(self, arr, k, x):
        """
        :type arr: List[int]
        :type k: int
        :type x: int
        :rtype: List[int]

        0(K-n) solution

        """
        
        # determine if the numner is inside or outside the list 
        ld = arr[0]-x 
        rd = arr[-1]-x 

        if ld*rd < 0: 
            # the number is inside the list: 
            li = 0
            ri = len(arr)-1
            while ri-li > k-1: 

                ld = arr[li]-x
                rd = arr[ri]-x 


                if abs(ld)>abs(rd): 
                    li += 1 

                elif abs(ld)<abs(rd): 
                    ri -= 1 

                else: 
                    ri -= 1

                print(ld, rd, li, ri)

            return arr[li:ri+1]

        elif ld*rd > 0 : 
            # outside of the loop 
            if x < arr[0]: 
                
                return arr[:k]

            else: 

                return arr[-k:]

        else: 
            if ld == 0: 
                return arr[:k]
            else: 
                return arr[-k:]

if __name__ == "__main__": 


    sol = Solution()

    arr = [1,2,3,4,5]
    k = 4
    x = 3

    arr = [1,2,3,4,5]
    k = 4
    x = 9

    arr = [1,2,3,4,5]
    k = 4
    x = -1

    arr = [0,1,4,6,7]
    k = 2
    x = 3

    arr = [1,2]
    k = 1
    x = 1 

    print(sol.findClosestElements(arr, k, x))