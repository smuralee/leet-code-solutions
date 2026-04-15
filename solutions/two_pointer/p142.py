from typing import Optional


class ListNode:
    def __init__(self, value: int, next: ListNode = None):
        self.value = value
        self.next = next


def detect_cycle(head: Optional[ListNode]) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            # Reset one pointer back to head
            # We have detected the existence of cycle
            # Increment by 1 step, when match found return that node
            slow = head
            while slow is not fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
