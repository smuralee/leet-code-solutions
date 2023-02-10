from typing import List


class Solution(object):
    def maxProfit(self, prices: List[int]):
        """
        :type prices: List[int]
        :rtype: int
        """
        if len(prices) == 1:
            return 0

        else:
            i, j = 0, 1
            buy, sell = prices[i], prices[j]
            res = 0

            while j < len(prices):

                if prices[j] > prices[i]:

                    sell = prices[j] if prices[j] > sell else sell
                    res = max(sell - buy, res)

                else:

                    if prices[j] < buy:
                        buy = prices[j]
                        sell = buy

                i += 1
                j += 1

        return res


if __name__ == '__main__':
    prices_1 = [7, 1, 5, 3, 6, 4]
    prices_2 = [7, 6, 4, 3, 1]
    prices_3 = [2, 4, 1]

    sol = Solution()

    print(sol.maxProfit(prices_1))
    print(sol.maxProfit(prices_2))
    print(sol.maxProfit(prices_3))
