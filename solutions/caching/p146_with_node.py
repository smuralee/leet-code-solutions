import time
from typing import Optional


class Node:
    __slots__ = ("key", "value", "prev", "next", "expires_at")

    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = self.next = None
        self.expires_at = float("inf")


class LRUCacheWithNode:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Invalid capacity value, cannot be zero or negative")
        self.capacity = capacity
        self.cache = {}
        self.head = Node()  # Sentinel node - LRU end
        self.tail = Node()  # Sentinel node - MRU end
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Unlink the node from the DLL"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_back(self, node: Node) -> None:
        """Move the node to the back of the DLL, before the sentinel node"""
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def _move_to_back(self, node: Node) -> None:
        self._remove(node)
        self._add_to_back(node)

    def _is_expired(self, node: Node) -> bool:
        return time.monotonic() > node.expires_at

    def _evict_node(self, node: Node) -> None:
        self._remove(node)
        del self.cache[node.key]

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        if self._is_expired(node):
            self._evict_node(node)
            return -1
        self._move_to_back(node)
        return node.value

    def put(self, key: int, value: int, ttl: Optional[float] = None) -> None:
        if ttl is not None and ttl <= 0:
            raise ValueError("TTL must be positive")
        if key in self.cache:
            self._evict_node(self.cache[key])
        node = Node(key, value)
        if ttl is not None:
            node.expires_at = time.monotonic() + ttl
        self.cache[key] = node
        self._add_to_back(node)
        if len(self.cache) > self.capacity:
            # Prefer evicting an expired node; fall back to LRU (head.next)
            node_to_evict = self.head.next
            curr = self.head.next
            while curr is not self.tail:
                if self._is_expired(curr):
                    node_to_evict = curr
                    break
                curr = curr.next
            self._evict_node(node_to_evict)
