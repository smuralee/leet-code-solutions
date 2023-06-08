# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __str__(self) -> str:
        res = ""
        while self:
            # print(self.next)
            res += f"{self.val}->"
            self = self.next
        return res


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if (not head) or (not head.next):
            print(head)
            return head

        print(head)
        p = self.reverseList(head.next)

        print(f"Ouput {p} from the previous call stack")
        print(f"Head value in the existing call stack:{head}")
        head.next.next = head
        print(f"Modified {p} from ")
        print(f"Head:{head}")
        print(p)
        print()
        return p


if __name__ == "__main__":
    node1 = ListNode(5, None)
    node2 = ListNode(4, node1)
    node3 = ListNode(3, node2)
    node4 = ListNode(2, node3)
    node5 = ListNode(1, node4)

    print("input")
    print(node5)
    print()

    s = Solution()
    print(s.reverseList(head=node5))
