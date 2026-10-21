"""Executable subset of the article's badge cases.

Covers TC-001..TC-029 logic without a browser: unread count, WebSocket-style
increments with dedup, mark-read decrement idempotency, mark-all-read,
99+ overflow cap, zero hides the badge, cross-tab sync, offline honesty,
reconnect resync, clear-vs-push race, expiry and the audit trail.
"""

import pytest

from badge_engine import (
    BadgeTab,
    BroadcastChannel,
    NotificationServer,
    make_bell,
)


@pytest.fixture()
def setup():
    server = NotificationServer()
    channel = BroadcastChannel()
    tab = make_bell(server, channel)
    return server, channel, tab


# -- positive cases ----------------------------------------------------


def test_badge_shows_unread_count(setup):  # TC-001
    server, _, tab = setup
    for i in range(5):
        server.push(f"n-{i}")
    tab.open()
    assert tab.display == "5"


def test_ws_push_increments_without_refresh(setup):  # TC-002
    server, _, tab = setup
    for i in range(3):
        server.push(f"n-{i}")
    tab.open()
    tab.push("n-42")
    assert tab.display == "4"


def test_mark_read_decrements_exactly_once(setup):  # TC-003 + idempotency edge
    server, _, tab = setup
    for i in range(5):
        server.push(f"n-{i}")
    tab.open()
    tab.mark_read("n-1")
    tab.mark_read("n-1")  # retried write is a no-op
    assert tab.display == "4"
    assert tab._count == 4


def test_mark_all_read_hides_badge(setup):  # TC-004 / TC-006
    server, _, tab = setup
    for i in range(10):
        server.push(f"n-{i}")
    tab.open()
    assert tab.display == "10"
    tab.mark_all_read()
    assert tab.display is None


def test_overflow_caps_at_99_plus(setup):  # TC-005
    server, _, tab = setup
    for i in range(150):
        server.push(f"n-{i}")
    tab.open()
    assert tab.display == "99+"
    assert server.unread_count() == 150  # cap is display-only, data keeps truth


def test_zero_never_renders_a_badge(setup):  # TC-017
    _, _, tab = setup
    assert tab.display is None


def test_badge_persists_across_sessions(setup):  # TC-007
    server, channel, _ = setup
    for i in range(7):
        server.push(f"n-{i}")
    new_tab = BadgeTab(server, channel)
    new_tab.open()  # "browser restart" — fresh view over the same server
    assert new_tab.display == "7"


# -- negative / sync cases ---------------------------------------------


def test_offline_tab_shows_no_phantom_increment(setup):  # TC-012
    server, channel, tab = setup
    for i in range(5):
        server.push(f"n-{i}")
    tab.open()
    tab.disconnect()
    server.push("n-off-1")
    server.push("n-off-2")
    assert tab._count == 5  # stale, not invented
    tab.reconnect()
    assert tab.display == "7"


def test_cross_tab_sync_converges(setup):  # TC-013
    server, channel, _ = setup
    tab_a = make_bell(server, channel)
    tab_b = make_bell(server, channel)
    for i in range(5):
        server.push(f"n-{i}")
    tab_a.open()
    tab_b.open()
    tab_a.mark_read("n-0")
    assert tab_b._count == 4  # broadcast converged without touching tab B


def test_duplicate_push_dedups(setup):  # boundary row 1
    server, _, tab = setup
    tab.push("n-42")
    tab.push("n-42")  # same message id delivered twice
    assert tab.display == "1"


def test_clear_all_then_inflight_push_lands_as_one(setup):  # boundary row 2
    server, _, tab = setup
    for i in range(10):
        server.push(f"n-{i}")
    tab.open()
    tab.mark_all_read()
    assert tab.display is None
    tab.push("n-late")  # in-flight during the clear lands as a fresh unread
    assert tab.display == "1"


def test_deleted_shared_notification_decrements(setup):  # TC-018
    server, channel, _ = setup
    tab_a = make_bell(server, channel)
    for i in range(3):
        server.push(f"n-{i}")
    tab_a.open()
    server.delete("n-1")
    tab_a._resync()
    assert tab_a.display == "2"


def test_expired_notifications_drop_from_count(setup):  # TC-029
    server, _, tab = setup
    for i in range(5):
        server.push(f"n-{i}")
    server.push("n-old-1", expires_in=30)
    server.push("n-old-2", expires_in=30)
    tab.open()
    assert tab.display == "7"
    server.tick(31)
    tab._resync()
    assert tab.display == "5"


def test_flood_counts_each_message_once(setup):  # TC-016
    server, _, tab = setup
    for i in range(50):
        tab.push(f"f-{i}")
        tab.push(f"f-{i}")  # double delivery under load
    assert server.unread_count() == 50
    assert tab.display == "50"


def test_every_change_is_audited(setup):  # TC-030
    server, _, tab = setup
    tab.push("n-1")
    tab.push("n-2")
    tab.mark_read("n-1")
    tab.mark_all_read()
    actions = [e["action"] for e in server.audit]
    assert actions == ["push", "push", "read", "clear_all"]
    read = server.audit[2]
    assert read["count_before"] == 2 and read["count_after"] == 1


def test_session_switch_shows_only_current_account():  # TC-028
    server_a = NotificationServer()
    server_b = NotificationServer()
    channel = BroadcastChannel()
    for i in range(5):
        server_a.push(f"a-{i}")
    for i in range(3):
        server_b.push(f"b-{i}")
    tab = make_bell(server_a, channel)
    assert tab.display == "5"
    tab.server = server_b  # account switch — view rebinds to the new account
    tab._resync()
    assert tab.display == "3"
