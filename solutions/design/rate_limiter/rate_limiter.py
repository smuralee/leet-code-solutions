from abc import ABC, abstractmethod
from typing import Optional
import time
import threading
import math
from collections import deque, defaultdict


class RateLimiter(ABC):
    @abstractmethod
    def allow(self, key: str, now: Optional[float] = None) -> bool:
        """
        Return True if the request is allowed, else False if rate-limited.
        """

    @abstractmethod
    def remaining(self, key: str, now: Optional[float] = None) -> int:
        """
        Return count of requests still allowed in the current window.
        """


class TokenBucket(RateLimiter):
    """
    Each key gets a bucket that fills at `rate` tokens/sec up to `capacity`.
    Each request consumes 1 token. Bursts up to `capacity` are allowed.

    Best for: APIs that want to allow short bursts but enforce average rate
    """

    def __init__(self, rate: float, capacity: int):
        self.rate = rate
        self.capacity = capacity
        self.buckets: dict[str, tuple[float, float]] = {}

    def _refill(self, key: str, now: float) -> float:
        if key not in self.buckets:
            self.buckets[key] = (float(self.capacity), now)
            return float(self.capacity)

        tokens, last_time = self.buckets[key]
        elapsed = now - last_time
        tokens = min(self.capacity, tokens + (elapsed * self.rate))
        self.buckets[key] = (tokens, now)
        return tokens

    def allow(self, key: str, now: Optional[float] = None) -> bool:
        ts = time.monotonic() if now is None else now
        tokens = self._refill(key, ts)
        if tokens >= 1.0:
            self.buckets[key] = (tokens - 1.0, ts)
            return True
        return False

    def remaining(self, key: str, now: Optional[float] = None) -> int:
        ts = time.monotonic() if now is None else now
        tokens = self._refill(key, ts)
        return int(tokens)


class LeakyBucket(RateLimiter):
    """
    Counts requests against a bucket that drains at a fixed rate.
    If the bucket is full, new requests are rejected (not queued).

    Difference from token bucket: leaky bucket enforces a STEADY output
    rate with no bursts. Token bucket allows bursts up to capacity.

    Best for: smoothing bursty input into steady output
    """

    def __init__(self, rate: float, capacity: int):
        self.rate = rate
        self.capacity = capacity
        self.buckets: dict[str, tuple[float, float]] = {}

    def _leak(self, key: str, now: float) -> float:
        if key not in self.buckets:
            self.buckets[key] = (0.0, now)
            return 0.0
        water, last_time = self.buckets[key]
        elapsed = now - last_time
        water = max(0.0, water - (elapsed * self.rate))
        self.buckets[key] = (water, now)
        return water

    def allow(self, key: str, now: Optional[float] = None) -> bool:
        ts = time.monotonic() if now is None else now
        water = self._leak(key, ts)
        if water + 1.0 <= self.capacity:
            self.buckets[key] = (water + 1.0, ts)
            return True
        return False

    def remaining(self, key: str, now: Optional[float] = None) -> int:
        ts = time.monotonic() if now is None else now
        if key not in self.buckets:
            return self.capacity
        water, last_time = self.buckets[key]
        water = max(0.0, water - ((ts - last_time) * self.rate))
        return max(0, int(self.capacity - water))


class FixedWindowCounter(RateLimiter):
    """
    Divides time into fixed windows of `window_seconds`.
    Each window allows up to `limit` requests.

    Pros: simple, O(1) memory per key
    Cons: boundary spike — a user can make 2x limit requests at the
          boundary of two windows (limit at end of w1 + limit at start of w2)

    Best for: when approximate is fine and simplicity matters
    """

    def __init__(self, limit: int, window_seconds: float = 60.0):
        self._limit = limit
        self._window = window_seconds
        self._counters: dict[str, tuple[int, int]] = {}

    def _window_id(self, ts: float) -> int:
        return int(ts // self._window)

    def allow(self, key: str, now: Optional[float] = None) -> bool:
        ts = time.monotonic() if now is None else now
        wid = self._window_id(ts)

        if key not in self._counters:
            self._counters[key] = (1, wid)
            return True

        count, stored_wid = self._counters[key]
        if stored_wid != wid:
            self._counters[key] = (1, wid)
            return True

        if count < self._limit:
            self._counters[key] = (count + 1, wid)
            return True

        return False

    def remaining(self, key: str, now: Optional[float] = None) -> int:
        ts = time.monotonic() if now is None else now
        wid = self._window_id(ts)

        if key not in self._counters:
            return self._limit
        count, stored_wid = self._counters[key]
        if stored_wid != wid:
            return self._limit
        return max(0, self._limit - count)


class SlidingWindowLog(RateLimiter):
    """
    Stores every request timestamp. Count = timestamps within the window.
    Exact but expensive: O(n) memory per key where n = requests in window.

    Best for: low-volume, high-accuracy requirements
    """

    def __init__(self, limit: int, window_seconds: float = 60.0):
        self._limit = limit
        self._window = window_seconds
        self._logs: dict[str, deque[float]] = defaultdict(deque)

    def _cleanup(self, key: str, now: float):
        cutoff = now - self._window
        log = self._logs[key]
        while log and log[0] <= cutoff:
            log.popleft()

    def allow(self, key: str, now: Optional[float] = None) -> bool:
        ts = time.monotonic() if now is None else now
        self._cleanup(key, ts)
        if len(self._logs[key]) < self._limit:
            self._logs[key].append(ts)
            return True
        return False

    def remaining(self, key: str, now: Optional[float] = None) -> int:
        ts = time.monotonic() if now is None else now
        self._cleanup(key, ts)
        return max(0, self._limit - len(self._logs[key]))


class SlidingWindowCounter(RateLimiter):
    """
    Combines fixed window counting with weighted interpolation from
    the previous window.

    count = current_window_count + previous_window_count × overlap_fraction
    overlap_fraction = 1 - (time_into_current_window / window_size)

    Pros: O(1) space per key, O(1) time, good approximation
    Cons: assumes uniform distribution in previous window
    """

    def __init__(self, limit: int, window_seconds: float = 60.0):
        self._limit = limit
        self._window = window_seconds
        # key → (current_count, previous_count, current_window_id)
        self._state: dict[str, tuple[int, int, int]] = {}

    def _window_id(self, ts: float) -> int:
        return int(ts // self._window)

    def _window_start(self, wid: int) -> float:
        return wid * self._window

    def _get_counts(self, key: str, ts: float) -> tuple[int, int, int]:
        """Return (current, previous, window_id) without mutating state."""
        wid = self._window_id(ts)
        if key not in self._state:
            return (0, 0, wid)

        current, previous, stored_wid = self._state[key]
        if wid > stored_wid:
            gap = wid - stored_wid
            if gap == 1:
                previous = current
            else:
                previous = 0
            current = 0
        return (current, previous, wid)

    def _weighted_count(self, key: str, ts: float) -> float:
        current, previous, wid = self._get_counts(key, ts)
        elapsed_in_window = ts - self._window_start(wid)
        overlap = 1.0 - (elapsed_in_window / self._window) if self._window > 0 else 0.0
        return current + previous * overlap

    def allow(self, key: str, now: Optional[float] = None) -> bool:
        ts = time.monotonic() if now is None else now
        if self._weighted_count(key, ts) >= self._limit:
            return False
        current, previous, wid = self._get_counts(key, ts)
        self._state[key] = (current + 1, previous, wid)
        return True

    def remaining(self, key: str, now: Optional[float] = None) -> int:
        ts = time.monotonic() if now is None else now
        used = self._weighted_count(key, ts)
        return max(0, math.ceil(self._limit - used))


class ThreadSafeRateLimiter(RateLimiter):
    """
    Wraps any RateLimiter with per-key lock striping.
    Uses N stripe locks instead of one global lock — keys that hash to
    different stripes can proceed concurrently.
    """

    def __init__(self, limiter: RateLimiter, num_stripes: int = 64):
        self.limiter = limiter
        self.stripes = [threading.Lock() for _ in range(num_stripes)]
        self.num_stripes = num_stripes

    def _stripe(self, key: str) -> threading.Lock:
        import zlib

        return self.stripes[zlib.crc32(key.encode()) % self.num_stripes]

    def allow(self, key: str, now: Optional[float] = None) -> bool:
        with self._stripe(key):
            return self.limiter.allow(key, now)

    def remaining(self, key: str, now: Optional[float] = None) -> int:
        with self._stripe(key):
            return self.limiter.remaining(key, now)
