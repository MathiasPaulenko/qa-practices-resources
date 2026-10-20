"""Pytest suite for the toast lifecycle state machine.

Each test maps to a case from the Toast Notification Test Cases resource
(https://qapractices.com/test-cases/toast-notification-auto-dismiss-test-cases/).
"""

from toast_lifecycle import State, ToastManager


def make_manager(**kwargs) -> ToastManager:
    return ToastManager(duration_ms=5000, **kwargs)


def test_auto_dismiss_fires_at_deadline():  # TC-001
    t = make_manager()
    toast = t.show("Order #4821 saved")
    t.tick(4999)
    assert toast.state == State.VISIBLE
    t.tick(1)
    assert toast.state == State.REMOVED


def test_toast_visible_before_deadline():  # TC-001
    t = make_manager()
    toast = t.show("Order #4821 saved")
    t.tick(4900)
    assert toast in t.visible


def test_persistent_toast_never_auto_dismisses():  # TC-011
    t = make_manager()
    toast = t.show("Sync failed", duration_ms=0, persistent=True)
    t.tick(10000)
    assert toast.state == State.VISIBLE


def test_timer_drift_within_tolerance():  # TC-012
    t = make_manager()
    toast = t.show("saved")
    t.tick(4800)
    assert toast.state == State.VISIBLE
    t.tick(199)
    assert toast.state == State.VISIBLE
    t.tick(1)
    assert toast.state == State.REMOVED


def test_pause_freezes_countdown():  # TC-004
    t = make_manager()
    toast = t.show("saved")
    t.tick(2000)
    t.pause(toast)
    t.tick(5000)
    assert toast.state == State.PAUSED


def test_resume_continues_from_remaining():  # TC-004
    t = make_manager()
    toast = t.show("saved")
    t.tick(2000)  # 3000ms remaining
    t.pause(toast)
    t.tick(5000)
    t.resume(toast)
    t.tick(2999)
    assert toast.state == State.VISIBLE
    t.tick(1)
    assert toast.state == State.REMOVED


def test_manual_close_cancels_timer():  # TC-005
    t = make_manager()
    toast = t.show("saved")
    t.close(toast)
    t.tick(10000)
    assert toast.state == State.REMOVED
    assert t.visible == []


def test_action_callback_fires_once():  # TC-006
    calls = []
    t = make_manager()
    toast = t.show("deleted", action=lambda: calls.append("undo"))
    assert t.click_action(toast)
    assert calls == ["undo"]
    assert toast.action_count == 1
    assert toast.state == State.REMOVED


def test_dead_click_after_dismiss_does_nothing():  # edge table
    calls = []
    t = make_manager()
    toast = t.show("deleted", action=lambda: calls.append("undo"))
    t.tick(5000)
    assert not t.click_action(toast)
    assert calls == []


def test_dismissed_toast_is_fully_removed():  # TC-010
    t = make_manager()
    toast = t.show("saved")
    t.tick(5000)
    assert toast not in t.visible
    assert toast.state == State.REMOVED


def test_stack_never_exceeds_max():  # TC-013
    t = make_manager(max_visible=3)
    for i in range(5):
        t.show(f"toast {i}")
    assert len(t.visible) == 3
    assert len(t.queue) == 2


def test_queue_drains_fifo():  # TC-024
    t = make_manager(max_visible=1)
    t.show("first")
    b = t.show("second")
    c = t.show("third")
    t.tick(5000)
    assert t.visible == [b]
    t.tick(5000)
    assert t.visible == [c]


def test_dedup_resets_timer():  # TC-017
    t = make_manager()
    a = t.show("saved")
    t.tick(4000)
    same = t.show("saved")
    assert same is a
    t.tick(4999)
    assert a.state == State.VISIBLE


def test_priority_preempts_lowest():  # TC-025
    t = make_manager(max_visible=3)
    for i in range(3):
        t.show(f"info {i}", priority=0)
    err = t.show("error", priority=10)
    assert err in t.visible
    assert len(t.visible) == 3


def test_low_priority_queues_when_full():  # TC-025
    t = make_manager(max_visible=1)
    high = t.show("error", priority=10)
    low = t.show("info", priority=0)
    assert t.visible == [high]
    assert t.queue == [low]


def test_paused_toast_does_not_expire():  # hover edge
    t = make_manager()
    toast = t.show("saved")
    t.pause(toast)
    t.tick(60000)
    assert toast.state == State.PAUSED


def test_no_duplicates_from_retry_burst():  # TC-030
    t = make_manager(max_visible=3)
    for _ in range(50):
        t.show("same message")
    assert len(t.visible) <= 3
    assert sum(1 for x in t.visible if x.message == "same message") == 1


def test_multiple_dismissals_safe():  # idempotent close
    t = make_manager()
    toast = t.show("saved")
    t.close(toast)
    t.close(toast)
    assert toast.state == State.REMOVED


def test_dequeue_only_on_vacancy():  # TC-024
    t = make_manager(max_visible=2)
    a = t.show("a")
    t.show("b")
    c = t.show("c")
    assert len(t.queue) == 1
    t.close(a)
    assert c in t.visible
    assert len(t.queue) == 0


def test_action_count_starts_at_zero():  # TC-006
    t = make_manager()
    toast = t.show("deleted", action=lambda: None)
    assert toast.action_count == 0
    t.click_action(toast)
    assert toast.action_count == 1
