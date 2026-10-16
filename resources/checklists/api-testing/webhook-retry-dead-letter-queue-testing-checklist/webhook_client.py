"""Reference webhook sender with retry, exponential backoff, jitter and DLQ routing.

Companion code for the Webhook Retry and Dead Letter Queue Testing Checklist:
https://qapractices.com/checklists/webhook-retry-dead-letter-queue-testing-checklist

The client retries transient failures (408, 429, 5xx, timeouts, connection
errors) with exponential backoff plus jitter, honors Retry-After, and routes
permanent failures and exhausted retries to an in-memory dead letter queue.
"""

import random
import time
from dataclasses import dataclass, field
from email.utils import parsedate_to_datetime
from typing import Callable, Optional

import requests

RETRIABLE_STATUS = {408, 429}
MAX_RETRIES = 4
BASE_DELAY = 1.0
MAX_DELAY = 30.0
JITTER = 0.3


@dataclass
class DeadLetter:
    """A delivery that could not be completed."""

    event_id: str
    payload: dict
    reason: str
    attempts: int
    timestamp: float = field(default_factory=time.time)


class RetryExhausted(Exception):
    """Raised when the retry budget is spent and the message is dead-lettered."""


class DLQ:
    """Minimal dead letter queue: holds failed deliveries for inspection/replay."""

    def __init__(self):
        self.messages: list[DeadLetter] = []

    def add(self, message: DeadLetter) -> None:
        if all(m.event_id != message.event_id for m in self.messages):
            self.messages.append(message)

    def replay(self, event_id: str, deliver: Callable[[dict, str], str]) -> str:
        """Re-send a dead-lettered message with its original event ID."""
        msg = next((m for m in self.messages if m.event_id == event_id), None)
        if msg is None:
            raise KeyError(f"event {event_id} not in DLQ")
        result = deliver(msg.payload, msg.event_id)
        if result == "delivered":
            self.messages.remove(msg)
        return result


def _retry_after_seconds(resp: requests.Response) -> Optional[float]:
    value = resp.headers.get("Retry-After")
    if not value:
        return None
    if value.isdigit():
        return float(value)
    try:
        return max(0.0, parsedate_to_datetime(value).timestamp() - time.time())
    except (TypeError, ValueError):
        return None


def _is_retriable(status: Optional[int]) -> bool:
    if status is None:  # timeout / connection error
        return True
    return status >= 500 or status in RETRIABLE_STATUS


def deliver_webhook(
    url: str,
    payload: dict,
    event_id: str,
    dlq: DLQ,
    max_retries: int = MAX_RETRIES,
    base_delay: float = BASE_DELAY,
    signer: Optional[Callable[[dict], dict]] = None,
    sleep: Optional[Callable[[float], None]] = None,
) -> str:
    """Deliver a webhook with exponential backoff + jitter and DLQ routing.

    Returns "delivered" or "dlq". Retries reuse the same event ID so the
    receiver can deduplicate; permanent 4xx go straight to the DLQ.
    """
    sleep = sleep or time.sleep
    headers = {"X-Event-Id": event_id, "X-Event-Timestamp": str(time.time())}
    if signer:
        headers.update(signer(payload))

    delay = base_delay
    for attempt in range(max_retries + 1):
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=5)
            status = resp.status_code
        except requests.RequestException:
            resp, status = None, None

        if status is not None and 200 <= status < 300:
            return "delivered"

        if status is not None and not _is_retriable(status):
            dlq.add(DeadLetter(event_id, payload, f"permanent_{status}", attempt + 1))
            return "dlq"

        if attempt >= max_retries:
            break

        wait = delay
        if resp is not None:
            retry_after = _retry_after_seconds(resp)
            if retry_after is not None:
                wait = max(delay, retry_after)
        sleep(wait * (1 + random.uniform(0, JITTER)))
        delay = min(delay * 2, MAX_DELAY)

    dlq.add(DeadLetter(event_id, payload, "max_retries", max_retries + 1))
    return "dlq"
