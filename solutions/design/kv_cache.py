from typing import Any
import time
from abc import ABC, abstractmethod


class Node:
    def __init__(self, key: str = "key", value: Any = None, ttl: float = float("inf")):
        self.key = key
        self.value = value
        if ttl < 0.0:
            raise ValueError("Invalid TTL value, less than 0.0 not allowed.")
        self.expiry_at = time.time() + ttl
        self.next = None
        self.prev = None
        self.freq = 1

    def is_expired(self):
        return time.time() >= self.expiry_at


class DoubleLinkedList:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None
        self.size -= 1

    def remove_from_last(self):
        if self.size == 0:
            return None
        node = self.tail.prev
        self.remove(node)
        return node


class Cache(ABC):
    @abstractmethod
    def get(self, key: str) -> Any: ...

    @abstractmethod
    def put(self, key: str, value: Any, ttl: float) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> bool: ...


class LRUCache(Cache):
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity cannot be 0 or less than 0")
        self.capacity = capacity
        self.key_map: dict[str, Node] = {}
        self.dll = DoubleLinkedList()

    def _move_to_front(self, node):
        self.dll.remove(node)
        self.dll.add_to_front(node)

    def _evict(self, node):
        self.dll.remove(node)
        del self.key_map[node.key]

    def get(self, key: str) -> Any:
        if key in self.key_map:
            node = self.key_map[key]
            if node.is_expired():
                self._evict(node)
                return None
            self._move_to_front(node)
            return node.value
        return None

    def put(self, key: str, value: Any, ttl: float = float("inf")) -> None:
        if ttl < 0.0:
            raise ValueError("Invalid TTL value, less than 0.0 not allowed.")

        if key in self.key_map:
            node = self.key_map[key]
            if node.is_expired():
                self._evict(node)
            else:
                node.value = value
                node.expiry_at = time.time() + ttl
                self._move_to_front(node)
                return

        if self.dll.size >= self.capacity:
            evicted_node = self.dll.remove_from_last()
            del self.key_map[evicted_node.key]

        node = Node(key, value, ttl)
        self.dll.add_to_front(node)
        self.key_map[key] = node

    def delete(self, key: str) -> bool:
        if key in self.key_map:
            node = self.key_map[key]
            self._evict(node)
            return True
        return False


class LFUCache(Cache):
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity cannot be 0 or less than 0")
        self.capacity = capacity
        self.key_map: dict[str, Node] = {}
        self.freq_map: dict[int, DoubleLinkedList] = {}
        self.min_freq = 1

    def _add_to_freq_list(self, node):
        if node.freq not in self.freq_map:
            self.freq_map[node.freq] = DoubleLinkedList()
        self.freq_map[node.freq].add_to_front(node)

    def _promote(self, node):
        freq_list = self.freq_map[node.freq]
        freq_list.remove(node)
        if freq_list.size == 0:
            del self.freq_map[node.freq]
            if node.freq == self.min_freq:
                self.min_freq += 1
        node.freq += 1
        self._add_to_freq_list(node)

    def _evict(self, node):
        self.freq_map[node.freq].remove(node)
        del self.key_map[node.key]
        if self.freq_map[node.freq].size == 0:
            del self.freq_map[node.freq]
            if node.freq == self.min_freq:
                self.min_freq = min(self.freq_map, default=1)

    def get(self, key: str) -> Any:
        """
        if key not in key_map:
            return None
        promote the node (see _promote):
            - remove from current freq list, drop bucket + bump min_freq if empty
            - increment node.freq and insert into the next freq list
        return node.value
        """
        if key not in self.key_map:
            return None
        node = self.key_map[key]
        if node.is_expired():
            self._evict(node)
            return None
        self._promote(node)
        return node.value

    def put(self, key: str, value: Any, ttl: float = float("inf")) -> None:
        """
        raise if ttl < 0.0
        if key in key_map:
            if node is expired: evict and fall through to new-node insert
            else: update node.value and node.expiry_at, promote (see _promote), return
        if at capacity:
            evict LRU node from the min_freq list
            drop the min_freq bucket if it is now empty
        create new node, insert into key_map and its freq list
        reset min_freq to 1 (new nodes always enter at freq 1)
        """
        if ttl < 0.0:
            raise ValueError("Invalid TTL value, less than 0.0 not allowed.")
        if key in self.key_map:
            node = self.key_map[key]
            if node.is_expired():
                self._evict(node)
            else:
                node.value = value
                node.expiry_at = time.time() + ttl
                self._promote(node)
                return

        if len(self.key_map) >= self.capacity:
            evicted_node = self.freq_map[self.min_freq].remove_from_last()
            del self.key_map[evicted_node.key]
            if self.freq_map[self.min_freq].size == 0:
                del self.freq_map[self.min_freq]

        node = Node(key, value, ttl)
        self.key_map[key] = node
        self._add_to_freq_list(node)
        self.min_freq = 1

    def delete(self, key: str) -> bool:
        if key in self.key_map:
            node = self.key_map[key]
            self._evict(node)
            return True
        return False
