from collections import defaultdict, deque
from time import monotonic
from typing import Callable, Deque, Dict

from fastapi import HTTPException, Request, status

from app.config import settings


class FixedWindowRateLimiter:
    """Small in-process limiter for API abuse protection.

    This is appropriate for local/dev and single-instance deployments. In a
    horizontally scaled production setup, back it with Redis using the same
    dependency interface.
    """

    def __init__(self):
        self._requests: Dict[str, Deque[float]] = defaultdict(deque)

    def check(self, key: str, limit: int, window_seconds: int) -> None:
        now = monotonic()
        bucket = self._requests[key]

        while bucket and now - bucket[0] >= window_seconds:
            bucket.popleft()

        if len(bucket) >= limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again shortly.",
            )

        bucket.append(now)


limiter = FixedWindowRateLimiter()


def _client_key(request: Request, scope: str) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    client_ip = forwarded_for.split(",")[0].strip()
    if not client_ip and request.client:
        client_ip = request.client.host
    if not client_ip:
        client_ip = "unknown"
    return f"{scope}:{client_ip}"


def rate_limit(limit_getter: Callable[[], int], scope: str):
    async def dependency(request: Request):
        limiter.check(
            _client_key(request, scope),
            limit_getter(),
            settings.RATE_LIMIT_WINDOW_SECONDS,
        )

    return dependency

