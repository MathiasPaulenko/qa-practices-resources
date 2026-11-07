"""Deterministic webhook provider/consumer pair for the qapractices.com suite.

Stdlib only. The clock is injected everywhere so retries, tolerance windows
and replay scenarios are reproducible — no real sleeping, no network.
"""

import hashlib
import hmac
import json

SCHEME = "t={ts},v1={sig}"


def sign(body: bytes, secret: str, ts: int) -> str:
    """Return a Stripe-style signature header for `body` at time `ts`."""
    sig = hmac.new(
        secret.encode(), f"{ts}.{body.decode()}".encode(), hashlib.sha256
    ).hexdigest()
    return SCHEME.format(ts=ts, sig=sig)


def verify_signature(body: bytes, header: str, secrets, now: int, tolerance: int = 300) -> bool:
    """Constant-time HMAC check plus timestamp tolerance (replay window).

    `secrets` is a list so a rotation window can hold more than one.
    """
    try:
        parts = dict(p.split("=", 1) for p in header.split(","))
        ts, sig = int(parts["t"]), parts["v1"]
    except (KeyError, ValueError, AttributeError):
        return False
    signed = f"{ts}.{body.decode()}".encode()
    for secret in secrets:
        expected = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
        if hmac.compare_digest(expected, sig):
            return (now - ts) <= tolerance
    return False


class Consumer:
    """A webhook receiver: verify -> parse -> dedup -> order -> apply."""

    def __init__(self, secrets, tolerance: int = 300, known_types=None):
        self.secrets = list(secrets)
        self.tolerance = tolerance
        self.known_types = set(known_types) if known_types else None
        self.seen = {}        # event_id -> delivery count
        self.last_created = {}  # object_id -> newest `created` applied
        self.effects = []     # applied side effects, for assertions
        self.log = []

    def receive(self, body: bytes, header, now: int):
        """Return (status_code, reason). Mirrors the suite's contract."""
        if header is None or not verify_signature(
            body, header, self.secrets, now, self.tolerance
        ):
            self.log.append("rejected: signature")
            return 401, "invalid_signature"
        try:
            event = json.loads(body)
        except json.JSONDecodeError:
            self.log.append("rejected: malformed")
            return 400, "malformed_json"
        if "type" not in event or "id" not in event:
            self.log.append("rejected: missing_fields")
            return 400, "missing_fields"

        event_id = event["id"]
        self.seen[event_id] = self.seen.get(event_id, 0) + 1
        if self.seen[event_id] > 1:
            self.log.append(f"duplicate: {event_id}")
            return 200, "duplicate"
        if self.known_types is not None and event["type"] not in self.known_types:
            self.log.append(f"ignored: {event['type']}")
            return 200, "ignored_type"

        obj = event.get("data", {}).get("object_id", event_id)
        created = event.get("created", 0)
        if created < self.last_created.get(obj, -1):
            self.log.append(f"stale: {event_id} (created={created})")
            return 200, "stale_event"

        self.last_created[obj] = created
        self.effects.append(event_id)
        self.log.append(f"processed: {event_id}")
        return 200, "processed"


class Provider:
    """Delivers an event with exponential backoff and a dead-letter path."""

    def __init__(self, schedule=(60, 300, 1800), max_attempts: int = 5):
        self.schedule = list(schedule)
        self.max_attempts = max_attempts
        self.attempts = []   # (attempt_no, scheduled_wait, status)
        self.dlq = []

    def deliver(self, endpoint, body: bytes, secret: str, start: int, jitter: float = 0.0):
        """Call `endpoint(body, header, now)` until 2xx or attempts exhausted."""
        now = start
        for attempt in range(1, self.max_attempts + 1):
            status, _ = endpoint(body, sign(body, secret, now), now)
            self.attempts.append((attempt, now, status))
            if 200 <= status < 300:
                return True
            if 400 <= status < 500 and status not in (408, 429):
                break  # 4xx is permanent — retrying can't help
            if attempt < self.max_attempts:
                wait = self.schedule[min(attempt - 1, len(self.schedule) - 1)]
                now += int(wait * (1 + jitter))
        self.dlq.append(body)
        return False


def validate_endpoint(scheme: str, cert_valid: bool, hostname_match: bool) -> bool:
    """Provider-side endpoint validation (TC-11): HTTPS + sound certificate."""
    return scheme == "https" and cert_valid and hostname_match
