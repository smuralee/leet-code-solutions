from collections import Counter


class Solution(object):
    def checkInclusion(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """
        count_map_s1, w, matched = Counter(s1), len(s1), 0

        # O(len(s2))
        for i in range(len(s2)):

            # decrease the count and increase the match 
            if s2[i] in count_map_s1:
                count_map_s1[s2[i]] -= 1
                if count_map_s1[s2[i]] == 0:
                    # if all occurences are matched, we claim it as a match 
                    matched += 1

                    # increase the count of the duplicate as we move further
            if i >= w and s2[i - w] in count_map_s1:
                # if all the occureances are matched for the previous character
                if count_map_s1[s2[i - w]] == 0:
                    # we still must remove 1 from the matched count, the reason is that the 
                    matched -= 1
                count_map_s1[s2[i - w]] += 1

                # print(s2[i],count_map_s1,matched)

            if matched == len(count_map_s1):
                return True
        return False


if __name__ == "__main__":
    # s1 = "aba"
    # s2 = "eidbaooo"
    s1 = "ab"
    s2 = "aabfc"
    sol = Solution()

    print(sol.checkInclusion(s1, s2))
