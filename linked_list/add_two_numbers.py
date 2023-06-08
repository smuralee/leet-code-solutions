from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:
        """_summary_

        Returns:
            _type_: _description_

        TC: O(N)
        sc: O(1)
        """

        c = 0
        res = l1
        while l1 and l2:
            l1_nxt = l1.next
            l2_nxt = l2.next

            if l2.next and not l1.next:
                l1.next = l2.next
                l1_nxt = l1.next
                l2_nxt = None

            l1.val, c = (l1.val + l2.val + c) % 10, (l1.val + l2.val + c) // 10

            if not l1_nxt and c != 0:
                l1.next = ListNode(c)
                c = 0
                break

            l1 = l1_nxt
            l2 = l2_nxt

        while l1:
            nxt = l1.next

            l1.val, c = (l1.val + c) % 10, (l1.val + c) // 10

            if not nxt and c != 0:
                l1.next = ListNode(c)
                c = 0
                break
            # print()

            l1 = nxt

        return res
