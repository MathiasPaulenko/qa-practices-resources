"""Client-side rate-limit harness: Retry-After parsing, backoff + jitter, SSE truncation check."""

import random
import time
from email.utils import parsedate_to_datetime

import requests


def parse_retry_after(value: str | None) -> float | None:
    """Parse `Retry-After` as either delta-seconds or an HTTP-date (RFC 9110)."""
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            return max(0.0, parsedate_to_datetime(value).timestamp() - time.time())
        except (TypeError, ValueError):
            return None


def call_with_backoff(url, headers, json_body=None, max_attempts=5, base_delay=1.0,
                      sleep=time.sleep, session=None):
    """POST until a non-429 answer or the retry cap; returns the last response."""
    sess = session or requests
    resp = None
    for attempt in range(max_attempts):
        resp = sess.post(url, headers=headers, json=json_body or {}, timeout=30)
        if resp.status_code != 429:
            return resp
        wait = parse_retry_after(resp.headers.get("Retry-After"))
        delay = wait if wait is not None else base_delay * (2 ** attempt)
        sleep(delay + random.uniform(0, delay * 0.25))
    return resp


def iter_sse_events(lines):
    """Yield `data:` payloads from an SSE line stream."""
    for raw in lines:
        line = raw.decode() if isinstance(raw, bytes) else raw
        line = line.strip()
        if line.startswith("data:"):
            yield line[5:].strip()


def stream_is_complete(chunks) -> bool:
    """An SSE reply is only final when it terminates with `data: [DONE]`."""
    return any(c == "[DONE]" for c in chunks)
