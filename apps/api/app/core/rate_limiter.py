import time
from typing import Dict, List
from fastapi import HTTPException, status
from app.core.config import settings

class InMemoryRateLimiter:
    """
    Sliding-window per-user in-memory rate limiter.
    Defaults to CHAT_RATE_LIMIT_PER_MINUTE requests per 60-second window.
    """
    def __init__(self, limit: int = None, window_seconds: int = 60):
        self.limit = limit or settings.CHAT_RATE_LIMIT_PER_MINUTE
        self.window_seconds = window_seconds
        self._user_requests: Dict[str, List[float]] = {}

    def check_rate_limit(self, user_id: str) -> None:
        now = time.time()
        window_start = now - self.window_seconds

        # Prune older entries
        timestamps = self._user_requests.get(user_id, [])
        valid_timestamps = [t for t in timestamps if t > window_start]

        if len(valid_timestamps) >= self.limit:
            oldest_in_window = valid_timestamps[0]
            retry_after = int(self.window_seconds - (now - oldest_in_window)) + 1
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.limit} requests per minute.",
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(now + retry_after))
                }
            )

        valid_timestamps.append(now)
        self._user_requests[user_id] = valid_timestamps

    def reset_for_user(self, user_id: str) -> None:
        if user_id in self._user_requests:
            del self._user_requests[user_id]

# Singleton instance
chat_rate_limiter = InMemoryRateLimiter()
