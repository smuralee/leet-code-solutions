from logging.config import valid_ident
from tkinter import S
from turtle import right
from numpy import record


class Solution(object):
    def minWindminiow(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
    
        """
        if len(t) > len(s): 
            return ""

        else:

            t_stats = {}
            for c in t: 
                t_stats[c] = t_stats.get(c,0)+1
            print(t_stats)

            l,r = 0,0 

            num_unique = len(t_stats)

            valid_string = 0 

            res = float("inf"), None, None 

            s_stats = {}
            while r < len(s): 
                
                # increase the count of the right pointer 
                s_stats[s[r]] = s_stats.get(s[r],0)+1 

                # compute the number of the valid_string when the stats count is matched 
                if s[r] in t_stats and s_stats[s[r]] == t_stats[s[r]]:
                    valid_string += 1 
                
                # increase the count of the left pointer 
                while l<=r and valid_string == len(t_stats):
                    
                    # update the result with the smallest window
                    if r-l+1 < res[0]:
                        res = (r-l+1, l, r)

                    # take away the data at the left pointer 
                    s_stats[s[l]] -= 1 
                    
                    # after reducing the count by 1, 
                    if s[l] in t_stats and s_stats[s[l]] < t_stats[s[l]]:
                        valid_string -=1  

                    l += 1 

                r += 1 

            return "" if res[0] == float("inf") else s[res[1] : res[2] + 1]




        
if __name__ == "__main__": 

    sol = Solution()
    
    s = "ADOBECODEBANC" 
    t = "ABC"
    
    print(sol.minWindminiow(s,t))