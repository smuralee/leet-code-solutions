from typing import Optional


class ListNode:

    __slots__ = ("value", "next")

    def __init__(self, value: int, next: ListNode = None):
        self.value = value
        self.next = next

    # Only value based equality, the nodes are mutable i.e. next can change
    # Due to mutable nodes, it is not hashable
    def __eq__(self, other):
        if not isinstance(other, ListNode):
            return NotImplemented
        return self.value == other.value

    __hash__ = None


def has_cycle(head: Optional[ListNode]) -> bool:
    slow = fast = head
    # Fast moves 2 steps, so ensure the current and next nodes are not None
    while fast and fast.next:
        # Slow pointer moves 1 step, fast pointer moves 2 steps
        # Assuming the gap between slow and fast pointer as "x"
        # Fast pointer always gains 1 step on the slow pointer
        # So the gap reduces by 1 and ultimately, the fast pointer will catch up to slow pointer
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
