#Definition for singly-linked list.
from typing import Optional 
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __str__(self) -> str:
        
        res = ''
        while self: 
            #print(self.next)
            res += f"{self.val}->"
            self = self.next
        return res 


class Solution:
    def test_1(self, head: ListNode) -> ListNode:
        if (not head) or (not head.next):
            #print(head)
            return head
        
        #print(head)
        p = self.test_1(head.next)
        
        head.next = p
        print(head)
        return head


if __name__ == "__main__": 

    node1 = ListNode(5,None)
    node2 = ListNode(4,node1)
    node3 = ListNode(3,node2)
    node4 = ListNode(2,node3)
    node5 = ListNode(1,node4)

    print('input')
    print(node5)
    print()

    s = Solution()
    print(s.test_1(
        head = node5
    ))

