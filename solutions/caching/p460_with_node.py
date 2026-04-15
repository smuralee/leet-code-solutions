from collections import defaultdict


class Node:
    __slots__ = ("key", "value", "next", "prev", "freq")

    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None
        self.freq = 1


class DoubleLinkedList:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_first(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def remove_last(self) -> Node:
        """
        Return the node so we can clean up the key_map
        """
        node = self.tail.prev
        self.remove(node)
        return node


class LFUCacheWithNode:
    def __init__(self, capacity: int):
        """
        freq_map groups nodes by how often they've been accessed.
        Frequency 1 has one linked list, frequency 2 has another, etc.
        Within each frequency list, position = recency.
        Front = most recent, back = oldest. So when evicting,
        we pick the back of the lowest-frequency list,
        giving us both "least frequently" and "least recently" used in O(1).
        """
        self.capacity = capacity
        self.key_map = {}  # key -> Node (for O(1) lookup)
        self.freq_map = defaultdict(
            DoubleLinkedList
        )  # frequency -> list of nodes with that frequency
        self.min_freq = 0  # tracks the current lowest frequency

    def _update(self, node):
        freq = node.freq
        self.freq_map[freq].remove(node)
        if self.min_freq == freq and self.freq_map[freq].size == 0:
            self.min_freq += 1
        node.freq += 1
        self.freq_map[node.freq].add_first(node)

    def get(self, key: int) -> int:
        if key not in self.key_map:
            return -1
        node = self.key_map[key]
        self._update(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.key_map:
            node = self.key_map[key]
            node.value = value
            self._update(node)
            return
        if len(self.key_map) == self.capacity:
            evicted = self.freq_map[self.min_freq].remove_last()
            del self.key_map[evicted.key]
        node = Node(key, value)
        self.key_map[key] = node
        self.freq_map[1].add_first(node)
        self.min_freq = 1
