from abc import ABC, abstractmethod
import time


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
        window: float,
        now: float | None = None,
    ) -> bool:
        """Consume one unit. True = request goes through, False = rejected.
        Rejected calls do NOT consume. Must be atomic per key."""

    @abstractmethod
    def remaining(
        self,
        key: str,
        limit: int,
        window: float,
        now: float | None = None,
    ) -> int:
        """Units left in the current window. Does not consume."""
