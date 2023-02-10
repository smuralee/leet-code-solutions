from numpy import record


class Solution(object):
    def minWindminiow(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
    
        """
        # build the target stats 
        t_stas = {}
        for c in t: 
            t_stas[c] = t_stas.get(c,0) + 1 

        sets = []
        record = []
        # build the non-overlapping occurence sets 
        # [(overlapping character, counts of the non-overlapping characters following)]
        for i in range(len(s)): 

            if s[i] in t_stas: 
                
                sets.append(record)

                record = []
                record.append(s[i])
                record.append(0)

                if i == len(s)-1: 
                    sets.append(record)

            else: 
                record[1]+= 1 

        # loop through the list and compute the 
        over_lap_count = 0 
        for i in sets: 
            
            

                

                

        print(sets[1:])

        
if __name__ == "__main__": 

    sol = Solution()
    
    s = "ADOBECODEBANC" 
    t = "ABC"
    
    print(sol.minWindminiow(s,t))