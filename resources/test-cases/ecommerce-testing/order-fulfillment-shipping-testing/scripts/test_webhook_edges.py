"""Edge-case assertions for tracking webhook handling.

Covers the rules exercised by TC-04, TC-08 and the edge-case table of the
order-fulfillment-shipping-testing resource:

- happy path: label_created → in_transit → out_for_delivery → delivered
- out-of-order events never regress a delivered status
- duplicate event_ids are idempotent (no state change, no extra notification)
- exception events are applied and flagged

Run:  pytest scripts/test_webhook_edges.py
"""

import json
from pathlib import Path

import pytest

from order_tracking_sim import OrderTracker

FIXTURE_DIR = Path(__file__).resolve().parent.parent / "carrier-webhooks"


def fixture(name: str) -> dict:
    with open(FIXTURE_DIR / name, encoding="utf-8") as fh:
        payload = json.load(fh)
    payload.pop("_note", None)
    return payload


def test_happy_path_reaches_delivered() -> None:
    tracker = OrderTracker(order_id="ORD-100482")
    for name in (
        "01-label-created.json",
        "02-in-transit.json",
        "03-out-for-delivery.json",
        "04-delivered.json",
    ):
        tracker.apply(fixture(name))

    assert tracker.status == "delivered"
    assert len(tracker.status_history) == 4
    assert len(tracker.notifications) == 4


def test_late_out_of_order_event_does_not_regress() -> None:
    tracker = OrderTracker(order_id="ORD-100482")
    for name in ("03-out-for-delivery.json", "04-delivered.json"):
        tracker.apply(fixture(name))

    result = tracker.apply(fixture("05-out-of-order-late-ofd.json"))

    assert tracker.status == "delivered"
    assert result["reason"] == "terminal_preserved"
    # History keeps the late event; the customer is not re-notified.
    assert len(tracker.status_history) == 3
    assert len(tracker.notifications) == 2


def test_duplicate_event_id_is_idempotent() -> None:
    tracker = OrderTracker(order_id="ORD-100482")
    tracker.apply(fixture("02-in-transit.json"))
    history_len = len(tracker.status_history)
    notifications_len = len(tracker.notifications)

    result = tracker.apply(fixture("06-duplicate-in-transit.json"))

    assert result == {
        "applied": False,
        "reason": "duplicate_event",
        "status": "in_transit",
    }
    assert len(tracker.status_history) == history_len
    assert len(tracker.notifications) == notifications_len


@pytest.mark.parametrize(
    "name,expected_code",
    [
        ("07-exception-lost.json", "LOST_IN_TRANSIT"),
        ("08-exception-damaged.json", "DAMAGED_RTS"),
    ],
)
def test_exceptions_are_applied_and_flagged(name: str, expected_code: str) -> None:
    tracker = OrderTracker(order_id="ORD-100482")
    tracker.apply(fixture("02-in-transit.json"))

    result = tracker.apply(fixture(name))

    assert result["reason"] == "exception"
    assert tracker.status == "exception"
    assert tracker.exception_code == expected_code
    assert any(n.startswith("exception:") for n in tracker.notifications)
