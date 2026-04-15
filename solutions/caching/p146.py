from collections import OrderedDict

"""
Instinct is to track "staleness", which is correct. But then you have to keep a timestamp.
Eviction requires an O(n) scan to find the minimum timestamp.

What OrderedDict fixes: it maintains access order via a linked list, 
so the least recent item is always at the front — eviction becomes O(1)
"""


class LRUCache:

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Invalid capacity value, cannot be zero or negative")
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        """
        Return the value of the key if the key exists, otherwise return -1.
        """
        if key not in self.cache:
            return -1
        # Keep the recent at the end and oldest at the front
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        """
        Update the value of the key if the key exists.
        Otherwise, add the key-value pair to the cache.
        If the number of keys exceeds the capacity from this operation,
        evict the least recently used key.
        """
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
