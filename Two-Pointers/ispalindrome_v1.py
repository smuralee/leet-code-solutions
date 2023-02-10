class Solution(object):
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """

        i = 0
        j = len(s) - 1

        res = False
        while j - i > 0:

            # print(s[i],s[j])

            if s[i].isalnum():

                if s[j].isalnum():

                    if s[i].lower() != s[j].lower():

                        print(f"Breaking point")
                        print(s[i], s[j])
                        return res

                    else:

                        i += 1
                        j -= 1

                else:
                    j -= 1

            else:

                if s[j].isalnum():
                    i += 1

                else:
                    i += 1
                    j -= 1

        res = True

        return res


if __name__ == "__main__":
    s1 = "A man, a plan, a canal: Panama"
    s2 = "race a car"

    sol = Solution()

    print(sol.isPalindrome(s1))
    print(sol.isPalindrome(s2))
