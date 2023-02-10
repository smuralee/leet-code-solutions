class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """

        if len(s) != 0:
            stats = {}

            history_max_length = 1
            current_max_length = 0
            current_start_index = 0

            for i, string in enumerate(s):

                if string in stats and stats[string] >= current_start_index:

                    current_max_length = i - stats[string]

                    current_start_index = stats[string] + 1

                    stats[string] = i

                else:

                    stats[string] = i

                    current_max_length += 1

                    history_max_length = max(history_max_length, current_max_length)

                # print(i, string)
                # print(current_max_length,history_max_length )

            return history_max_length
        else:
            return 0


if __name__ == '__main__':
    s = 'babcedfgb'
    s_2 = "abcabcbb"
    s_3 = "ba"
    s_4 = 'pwwkew'

    sol = Solution()
    print(sol.lengthOfLongestSubstring(s))
    print(sol.lengthOfLongestSubstring(s_2))
    print(sol.lengthOfLongestSubstring(s_3))
    print(sol.lengthOfLongestSubstring(s_4))

    #     stats = {
    #         'character' : the most recent position 
    #     }

    #     history_maximum_length = 1 [default]
    #         (only update if there we observe another value higher than it)

    #     iterate throught the list using both index and the value, 
    #         if current max length greater than historical max lenth 

    #             hitorical max length = current length 

    #         update the current max length by += 1 

    #     if the charaters is in the stats: 

    #         -> means that we found a repetition 

    #         -> current maximum length will reset to current_index - stats[the character]

    #         -> update the stats dictionary 

    #     012345678
    #     babcedfgb
    # h   122345676
    # c   122345677
