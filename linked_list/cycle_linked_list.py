# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def hasCycle_two_pointers(self, head: Optional[ListNode]) -> bool:
        tor, hair = head, head

        while hair and hair.next:
            tor = tor.next
            hair = hair.next.next

            if tor == hair:
                return True

        return False

    def hasCycle_hash_set(self, head: Optional[ListNode]) -> bool:
        visted = set()

        curr = head
        while curr:
            if curr not in visted:
                visted.add(curr)
            else:
                return True

            curr = curr.next

        return False
