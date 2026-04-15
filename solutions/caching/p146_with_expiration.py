from collections import OrderedDict
import time
from typing import Optional

"""
Instinct is to track "staleness", which is correct. But then you have to keep a timestamp.
Eviction requires an O(n) scan to find the minimum timestamp.

What OrderedDict fixes: it maintains access order via a linked list, 
so the least recent item is always at the front — eviction becomes O(1)

Here we are adding a expiry time as well to decide the eviction policy
"""


class LRUCacheWithExpiration:

    def __init__(self, capacity: int, default_ttl: Optional[float] = None) -> None:
        if capacity <= 0:
            raise ValueError("Invalid capacity value, cannot be zero or negative")
        if default_ttl is not None and default_ttl <= 0:
            raise ValueError("TTL must be positive")
        self.capacity = capacity
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.expiry = {}

    def _is_expired(self, key: int) -> bool:
        if key not in self.expiry:
            return False
        return time.monotonic() > self.expiry[key]

    def _evict(self, key: int):
        del self.cache[key]
        self.expiry.pop(key, None)

    def get(self, key: int) -> int:
        """
        Return the value of the key if the key exists, otherwise return -1.
        Evict the key if the TTL has expired
        """
        if key not in self.cache:
            return -1
        if self._is_expired(key):
            self._evict(key)
            return -1
        # Keep the recent at the end and oldest at the front
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int, ttl: Optional[float] = None) -> None:
        """
        Update the value of the key if the key exists.
        Otherwise, add the key-value pair to the cache.
        If the number of keys exceeds the capacity from this operation,
        evict the least recently used key.
        """
        if ttl is not None and ttl <= 0:
            raise ValueError("TTL must be positive")

        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value

        ttl = ttl if ttl is not None else self.default_ttl
        if ttl is not None:
            self.expiry[key] = time.monotonic() + ttl
        elif key in self.expiry:
            del self.expiry[key]

        if len(self.cache) > self.capacity:
            oldest_key, _ = self.cache.popitem(last=False)
            self.expiry.pop(oldest_key, None)
