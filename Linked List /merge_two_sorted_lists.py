# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        if not list1 or not list2:
            if list1 and not list2:
                return list1

            elif not list1 and list2:
                return list2

            else:
                return None

        else:
            if list1.val > list2.val:
                next_head = self.mergeTwoLists(list1, list2.next)
                list2.next = next_head
                return list2

            else:
                print(list1)
                next_head = self.mergeTwoLists(list1.next, list2)
                list1.next = next_head
                print(list1)
                print()
                return list1
