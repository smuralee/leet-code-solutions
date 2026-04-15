from __future__ import annotations

import time, threading, heapq
from enum import Enum
from typing import Any, Optional

_MISSING = object()


class Node:
    def __init__(self, key: str, value: Any, ttl: float = 0.0):
        self.key = key
        self.value = value
        self.expires_at = 0.0 if ttl <= 0 else time.monotonic() + ttl
        self.freq = 1
        self.next: Optional[Node] = None
        self.prev: Optional[Node] = None

    def is_expired(self) -> bool:
        return time.monotonic() >= self.expires_at > 0


class DoubleLinkedList:
    def __init__(self):
        self.head: Node = Node("", None)
        self.tail: Node = Node("", None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_to_front(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        node.next = None
        node.prev = None
        self.size -= 1

    def remove_last(self) -> Optional[Node]:
        if self.size == 0:
            return None
        node = self.tail.prev
        self.remove(node)
        return node


class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity cannot be zero or less than zero.")
        self.capacity = capacity
        self.key_map: dict[str, Node] = {}
        self.list = DoubleLinkedList()

    def _evict(self, node: Node) -> None:
        self.list.remove(node)
        del self.key_map[node.key]

    def _move_to_front(self, node: Node) -> None:
        self.list.remove(node)
        self.list.add_to_front(node)

    def get(self, key: str) -> Any:
        if key not in self.key_map:
            return _MISSING
        node = self.key_map[key]
        if node.is_expired():
            self._evict(node)
            return _MISSING
        self._move_to_front(node)
        return node.value

    def get_node(self, key: str) -> Optional[Node]:
        return self.key_map.get(key)

    def put(self, key: str, value: Any, ttl: float = 0.0):
        if key in self.key_map:
            node = self.key_map[key]
            if node.is_expired():
                self._evict(node)
            else:
                node.value = value
                node.expires_at = 0.0 if ttl <= 0 else time.monotonic() + ttl
                self._move_to_front(node)
                return
        if self.list.size >= self.capacity:
            evicted_node = self.list.remove_last()
            if evicted_node:
                del self.key_map[evicted_node.key]
        node = Node(key, value, ttl)
        self.list.add_to_front(node)
        self.key_map[key] = node

    def delete(self, key: str) -> bool:
        if key in self.key_map:
            self._evict(self.key_map[key])
            return True
        return False

    def __len__(self) -> int:
        return len(self.key_map)

    def __contains__(self, key: str) -> bool:
        if key not in self.key_map:
            return False
        return not self.key_map[key].is_expired()


class LFUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity cannot be zero or less than zero.")
        self.capacity = capacity
        self.key_map: dict[str, Node] = {}
        self.freq_map: dict[int, DoubleLinkedList] = {}
        self.min_freq = 1

    def _detach_node(self, node: Node):
        freq = node.freq
        freq_list = self.freq_map[freq]
        freq_list.remove(node)
        if freq_list.size == 0:
            del self.freq_map[freq]

    def _update_freq(self, node: Node):
        self._detach_node(node)
        if node.freq == self.min_freq and node.freq not in self.freq_map:
            self.min_freq += 1
        node.freq += 1
        if node.freq not in self.freq_map:
            self.freq_map[node.freq] = DoubleLinkedList()
        self.freq_map[node.freq].add_to_front(node)

    def _evict(self, node: Node):
        self._detach_node(node)
        del self.key_map[node.key]
        if self.key_map and self.min_freq not in self.freq_map:
            self.min_freq = min(self.freq_map)

    def get(self, key: str) -> Any:
        if key not in self.key_map:
            return _MISSING
        node = self.key_map[key]
        if node.is_expired():
            self._evict(node)
            return _MISSING
        self._update_freq(node)
        return node.value

    def get_node(self, key: str) -> Optional[Node]:
        return self.key_map.get(key)

    def put(self, key: str, value: Any, ttl: float = 0.0):
        if key in self.key_map:
            node = self.key_map[key]
            if node.is_expired():
                self._evict(node)
            else:
                node.value = value
                node.expires_at = 0.0 if ttl <= 0 else time.monotonic() + ttl
                self._update_freq(node)
                return

        if len(self.key_map) >= self.capacity:
            eviction_list = self.freq_map.get(self.min_freq)
            if eviction_list:
                evicted_node = eviction_list.remove_last()
                if evicted_node:
                    del self.key_map[evicted_node.key]
                    if eviction_list.size == 0:
                        del self.freq_map[self.min_freq]

        node = Node(key, value, ttl)
        self.key_map[key] = node
        if 1 not in self.freq_map:
            self.freq_map[1] = DoubleLinkedList()
        self.freq_map[1].add_to_front(node)
        self.min_freq = 1

    def delete(self, key: str) -> bool:
        if key in self.key_map:
            self._evict(self.key_map[key])
            return True
        return False

    def __len__(self) -> int:
        return len(self.key_map)

    def __contains__(self, key: str) -> bool:
        if key not in self.key_map:
            return False
        return not self.key_map[key].is_expired()


class Policy(Enum):
    LRU = LRUCache
    LFU = LFUCache


class KVCache:
    def __init__(self, capacity: int, policy: Policy = Policy.LRU):
        self._capacity = capacity
        self._cache = policy.value(capacity)

    def get(self, key: str) -> Any:
        result = self._cache.get(key)
        return None if result is _MISSING else result

    def put(self, key: str, value: Any, ttl: float = 0.0) -> None:
        self._cache.put(key, value, ttl)

    def delete(self, key: str) -> bool:
        return self._cache.delete(key)


class Metrics:
    __slots__ = ("_hits", "_misses", "_evictions", "_expired", "_lock")

    def __init__(self):
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expired = 0
        self._lock = threading.Lock()

    def record_hit(self):
        with self._lock:
            self._hits += 1

    def record_miss(self):
        with self._lock:
            self._misses += 1

    def record_eviction(self):
        with self._lock:
            self._evictions += 1

    def record_expired(self):
        with self._lock:
            self._expired += 1

    @property
    def hit_rate(self):
        with self._lock:
            total = self._hits + self._misses
            return self._hits / total if total else 0.0

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "hits": self._hits,
                "misses": self._misses,
                "evictions": self._evictions,
                "expired": self._expired,
                "hit_rate": (
                    self._hits / (self._hits + self._misses)
                    if (self._hits + self._misses)
                    else 0.0
                ),
            }


class Shard:
    def __init__(self, capacity: int, policy: Policy, metrics: Metrics):
        self.lock = threading.Lock()
        self.cache = policy.value(capacity)
        self.metrics = metrics
        self.expiry_heap: list[tuple[float, str]] = []

    def get(self, key: str) -> Any:
        with self.lock:
            node = self.cache.get_node(key)
            if node is not None and node.is_expired():
                self.cache.delete(key)
                self.metrics.record_expired()
                self.metrics.record_miss()
                return None
            result = self.cache.get(key)
            if result is _MISSING:
                self.metrics.record_miss()
                return None
            self.metrics.record_hit()
            return result

    def put(self, key: str, value: Any, ttl: float = 0.0) -> None:
        with self.lock:
            is_new = True
            node = self.cache.get_node(key)
            if node is not None:
                if node.is_expired():
                    self.cache.delete(key)
                    self.metrics.record_expired()
                else:
                    is_new = False
            old_size = len(self.cache)
            self.cache.put(key, value, ttl)
            if is_new and len(self.cache) == old_size:
                self.metrics.record_eviction()
            if ttl > 0:
                heapq.heappush(self.expiry_heap, (time.monotonic() + ttl, key))

    def delete(self, key: str) -> bool:
        with self.lock:
            return self.cache.delete(key)

    def __contains__(self, key: str) -> bool:
        with self.lock:
            return key in self.cache

    def __len__(self) -> int:
        with self.lock:
            return len(self.cache)

    def cleanup_expired(self, max_checks: int = 50) -> int:
        removed = 0
        now = time.monotonic()
        with self.lock:
            while self.expiry_heap and removed < max_checks:
                earliest, key = self.expiry_heap[0]
                if earliest > now:
                    break
                heapq.heappop(self.expiry_heap)
                node = self.cache.get_node(key)
                if node is not None and node.is_expired():
                    self.cache.delete(key)
                    self.metrics.record_expired()
                    removed += 1
        return removed


class ExpirationCleaner:
    def __init__(self, shards: list[Shard], interval: float = 1.0):
        self.shards = shards
        self.interval = interval
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join(timeout=self.interval * 2)

    def _run(self):
        while not self.stop_event.is_set():
            for shard in self.shards:
                shard.cleanup_expired()
            self.stop_event.wait(self.interval)


class KVStoreSharded:
    def __init__(
        self,
        capacity: int,
        policy: Policy = Policy.LRU,
        num_shards: int = 16,
        cleanup_interval: float = 1.0,
    ):
        self._capacity = capacity
        self._num_shards = num_shards
        self._metrics = Metrics()
        shard_capacity = max(1, capacity // num_shards)
        self._shards = [
            Shard(shard_capacity, policy, self._metrics) for _ in range(num_shards)
        ]
        self._cleaner = ExpirationCleaner(self._shards, cleanup_interval)
        self._cleaner.start()

    def _shard_for(self, key: str) -> Shard:
        return self._shards[hash(key) % self._num_shards]

    def get(self, key: str) -> Any:
        return self._shard_for(key).get(key)

    def put(self, key: str, value: Any, ttl: float = 0.0) -> None:
        self._shard_for(key).put(key, value, ttl)

    def delete(self, key: str) -> bool:
        return self._shard_for(key).delete(key)

    def __contains__(self, key: str) -> bool:
        return key in self._shard_for(key)

    def __len__(self) -> int:
        return sum(len(s) for s in self._shards)

    @property
    def metrics(self) -> dict[str, Any]:
        return self._metrics.snapshot()

    def shutdown(self):
        self._cleaner.stop()
