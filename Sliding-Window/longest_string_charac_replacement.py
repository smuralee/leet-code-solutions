class Solution(object):
    def characterReplacement(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        res = 0
        count = {}

        l = 0
        max_f = 0

        for r in range(len(s)):

            count[s[r]] = count.get(s[r], 0) + 1
            max_f = max(max_f, count[s[r]])

            print(l, r, max_f)

            if r - l + 1 - max_f > k:
                count[s[l]] = count.get(s[l], 0) - 1
                l += 1

            res = max(res, r - l + 1)

        return res


if __name__ == '__main__':
    sol = Solution()

    print(sol.characterReplacement('AABABBA', 1))

    ## Idea 

    """
    ABABBA k=2

    1. left pointer = 0 
        right_pointer = 0 
        stats[right_pointer] += 1 

    2. move index, right_pointer += 1, terminate: right_pointer = len(input)

        update the dict / max value 
        
        if len(right_pointer)-len(left_pointer)+1 - max(stats.values) <= k: 
            continue 
        else: 
            move the left pointer by one, 
            stats[left_pointer] += 1 

        stats[right_pointer] += 1 §

    """
