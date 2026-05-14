from abc import ABC, abstractmethod
import time
from collections import deque


class RateLimiter(ABC):
    """
    Per-key rate limiter. Subclasses pick the algorithm.

    `limit` and `window` are passed per-call so a single limiter instance can
    serve many policies (e.g., "100/min for /search, 10/min for /login").
    State is keyed only by `key` — changing limits doesn't invalidate buckets.
    """

    @abstractmethod
    def allowed(
        self,
        key: str,
        limit: int,
        window_seconds: float,
        now: float | None = None,
    ) -> bool:
        """Consume one unit. True = request goes through, False = rejected.
        Rejected calls do NOT consume. Must be atomic per key."""

    @abstractmethod
    def remaining(
        self,
        key: str,
        limit: int,
        window_seconds: float,
        now: float | None = None,
    ) -> int:
        """Units left in the current window. Does not consume."""


class LeakyBucket(RateLimiter):
    """
    Insights:
        - Schedule advances at a constant rate (interval = window / limit)
        - Extra requests beyond capacity are discarded
        - Allows an instantaneous burst of up to `limit` requests, then paces
          subsequent admits at `interval` apart until the schedule catches up
        - Provides stable long-run traffic control with bounded burstiness
    """

    def __init__(self):
        # State: { key: last_outflow_time }
        # This implementation uses the "Virtual Scheduling Algorithm"
        # (Leaky Bucket as a Meter)
        self.state = {}

    def allowed(
        self, key: str, limit: int, window_seconds: float, now: float | None = None
    ) -> bool:
        now = time.time() if now is None else now
        interval = window_seconds / limit  # Time required between requests

        # next_allowed_time is when the bucket will have "leaked" enough to allow a request
        next_allowed_time = self.state.get(key, now)

        # If the bucket is empty, start from 'now', otherwise add interval to the schedule
        new_next_allowed = max(now, next_allowed_time) + interval

        # If the next allowed time is too far in the future, we are at capacity
        if new_next_allowed > now + window_seconds:
            return False

        self.state[key] = new_next_allowed
        return True

    def remaining(
        self, key: str, limit: int, window_seconds: float, now: float | None = None
    ) -> int:
        now = time.time() if now is None else now
        next_allowed_time = self.state.get(key, now)
        time_until_empty = max(0, next_allowed_time - now)
        return int((window_seconds - time_until_empty) / (window_seconds / limit))


class TokenBucket(RateLimiter):
    """
    Insights:
        - Token refill rate is consistent
        - Extra tokens are discarded
        - Provides a burst request upto bucket capacity
        - Memory consumption due to separate bucket
        - Does not provide smooth request rate
    """

    def __init__(self):
        # State: { key: (current_tokens, last_updated_timestamp) }
        self.state: dict[str, tuple[float, float]] = {}

    def allowed(
        self, key: str, limit: int, window_seconds: float, now: float | None = None
    ) -> bool:
        now = time.time() if now is None else now
        fill_rate = limit / window_seconds

        # Return the limit and current time by default
        tokens, last_update = self.state.get(key, (limit, now))

        # 1. Refill: How much time passed * tokens per second
        elapsed = now - last_update
        tokens = min(limit, tokens + (elapsed * fill_rate))

        # 2. Consume
        if tokens >= 1:
            self.state[key] = (tokens - 1, now)
            return True

        self.state[key] = (tokens, now)
        return False

    def remaining(
        self, key: str, limit: int, window_seconds: float, now: float | None = None
    ) -> int:
        now = time.time() if now is None else now
        tokens, last_update = self.state.get(key, (limit, now))
        elapsed = now - last_update
        current_tokens = min(limit, tokens + (elapsed * (limit / window_seconds)))
        return int(current_tokens)


class FixedWindowCounter(RateLimiter):
    """
    Insights:
        - Divides time into fixed windows using time.time()//window_seconds i.e. buckets
        - Allows burst in the window duration
        - Window boundary issues, with max of twice the limit
        - Simple strategy for steady traffic
    """

    def __init__(self):
        # State : {key: {window_id, count}}
        self.state: dict[str, dict[int, int]] = {}

    def _get_window(self, window_seconds: float, now: float) -> int:
        # While the response is a whole number, it is still a float. Hence, cast to int
        return int(now // window_seconds)

    def allowed(
        self, key: str, limit: int, window_seconds: float, now: float | None = None
    ) -> bool:
        now = time.time() if now is None else now
        win_id = self._get_window(window_seconds, now)

        bucket = self.state.get(key)
        if bucket is None or win_id not in bucket:
            self.state[key] = {win_id: 1}
            return True

        count = bucket[win_id]
        if count < limit:
            bucket[win_id] = count + 1
            return True
        return False

    def remaining(
        self, key: str, limit: int, window_seconds: float, now: float | None = None
    ) -> int:
        now = time.time() if now is None else now
        win_id = self._get_window(window_seconds, now)

        if key not in self.state or win_id not in self.state[key]:
            return limit

        count = self.state[key][win_id]
        return max(0, limit - count)


class SlidingWindowLog(RateLimiter):
    """
    Insights:
        - Dynamic window, shift continuously with time
        - Smoother traffic control
        - Logs the timestamp of the requests, expires old entries and shifts the window
        - Addresses the boundary spike issue
    """

    def __init__(self):
        # State: { key: deque([ts1, ts2, ...]) }
        self.state: dict[str, deque[float]] = {}

    def allowed(
        self, key: str, limit: int, window_seconds: float, now: float | None = None
    ) -> bool:
        now = time.time() if now is None else now
        if key not in self.state:
            self.state[key] = deque()

        # read the oldest entry onwards in the deque and remove if outside the boundary
        log = self.state[key]
        while log and log[0] < now - window_seconds:
            log.popleft()

        # Add the new entries, if count within the limit
        if len(log) < limit:
            log.append(now)
            return True
        return False

    def remaining(
        self, key: str, limit: int, window_seconds: float, now: float | None = None
    ) -> int:
        now = time.time() if now is None else now
        log = self.state.get(key, deque())
        valid = sum(1 for ts in log if ts >= now - window_seconds)
        return max(0, limit - valid)


class SlidingWindowCounter(RateLimiter):
    """
    Insights:
        - Does not keep the timestamp for the requests
        - It does the approximation of the requests in adjacent windows

    count = current_window_count + previous_window_count x overlap_fraction
    overlap_fraction = 1 - (time_into_current_window / window_size)
    """

    def __init__(self):
        # State: {key: {window_id : count}}
        self.state: dict[str, dict[int, int]] = {}

    def allowed(
        self, key: str, limit: int, window_seconds: float, now: float | None = None
    ) -> bool:
        """
        Because windows are indexed by int(now // window_seconds) — consecutive integer buckets with no gaps.
        So the window immediately before curr_wind is always curr_wind - 1.

        A sliding window of length window_seconds ending at now can overlap at most two fixed buckets.
        The current one and the one right before it. Anything older than curr_wind - 1 is entirely
        outside the lookback range, so it can't contribute.
        """
        now = time.time() if now is None else now
        curr_win = int(now // window_seconds)
        prev_win = curr_win - 1

        if key not in self.state:
            self.state[key] = {}

        counts = self.state[key]

        # Evict anything older than prev_win — it can never contribute.
        for win in list(counts):
            if win < prev_win:
                del counts[win]

        # Math: How much of the current window have we covered?
        # (now % window_seconds) gives seconds into current window
        # We want to know what is the remainder beyond the bucket division by the window_seconds
        # dividend = quotient*divisor + remainder, we need the overlap i.e. remainder
        # Example:
        # now = 150s
        # current bucket started at 120s since we have 60s buckets
        # seconds into bucket = 150s - 120s = 30s

        # Doing that the long way:
        # 1. Find which bucket we're in: floor(150s / 60s) = 2 (the 3rd bucket)
        # 2. Find when it started: 2 * 60s = 120s
        # 3. Subtract: 150s - 120s = 30s
        # We get the same output with 150s % 60s

        overlap_fraction = 1 - ((now % window_seconds) / window_seconds)

        curr_count = counts.get(curr_win, 0)
        prev_count = counts.get(prev_win, 0)

        estimated_count = curr_count + (prev_count * overlap_fraction)

        # +1 so a request that would push us over the limit is rejected,
        # rather than admitted-then-overshooting on fractional estimates.
        if estimated_count + 1 <= limit:
            counts[curr_win] = curr_count + 1
            return True
        return False

    def remaining(
        self, key: str, limit: int, window_seconds: float, now: float | None = None
    ) -> int:
        now = time.time() if now is None else now
        curr_win = int(now // window_seconds)
        prev_win = curr_win - 1
        counts = self.state.get(key, {})

        overlap_fraction = 1 - ((now % window_seconds) / window_seconds)
        estimated_count = counts.get(curr_win, 0) + (
            counts.get(prev_win, 0) * overlap_fraction
        )

        return max(0, int(limit - estimated_count))
