"""Minimal order-tracking state machine implementing the rules under test.

Mirrors the expected behavior from the fulfillment test cases resource:
- every applied event is recorded in status history
- duplicate event_ids are idempotent (no state change, no notification)
- status never regresses once the shipment is delivered
- exception events are always applied and flagged

Replace `apply()` internals with a call to your real webhook handler when
testing against an actual service.
"""

TERMINAL_STATUSES = {"delivered", "returned_to_sender", "cancelled"}


class OrderTracker:
    """Tracks one shipment's status history and customer notifications."""

    def __init__(self, order_id: str) -> None:
        self.order_id = order_id
        self.status = "created"
        self.exception_code: str | None = None
        self.status_history: list[dict] = []
        self.notifications: list[str] = []
        self._seen_event_ids: set[str] = set()

    def apply(self, event: dict) -> dict:
        """Apply a carrier tracking event. Returns a result summary."""
        event_id = event["event_id"]

        if event_id in self._seen_event_ids:
            return {"applied": False, "reason": "duplicate_event", "status": self.status}
        self._seen_event_ids.add(event_id)

        status = event["status"]
        self.status_history.append(
            {"status": status, "occurred_at": event["occurred_at"], "event_id": event_id}
        )

        if status == "exception":
            self.exception_code = event.get("exception_code")
            self.status = "exception"
            self._notify(f"exception:{event['status_detail']}")
            return {"applied": True, "reason": "exception", "status": self.status}

        if self.status in TERMINAL_STATUSES:
            # Recorded for history, but a late event cannot regress a terminal status.
            return {"applied": True, "reason": "terminal_preserved", "status": self.status}

        self.status = status
        self._notify(f"status:{status}")
        return {"applied": True, "reason": "status_changed", "status": self.status}

    def _notify(self, message: str) -> None:
        self.notifications.append(message)
