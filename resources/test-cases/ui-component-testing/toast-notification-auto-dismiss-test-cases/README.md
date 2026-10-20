# Toast Notification Lifecycle Test Lab

Runnable companion for [Toast Notification Test Cases: 30 Auto-dismiss Scenarios](https://qapractices.com/test-cases/toast-notification-auto-dismiss-test-cases/) — a stdlib-only Python state machine that mirrors the toast contract (mount, countdown, pause-on-hover, stacking cap, queue, dedup, priority preemption, manual and action exits) plus a pytest suite exercising the failure modes from the resource.

## Run

```bash
pip install -r requirements.txt
pytest -v
```

## What it covers

| Test | Suite case |
|---|---|
| `test_auto_dismiss_fires_at_deadline` / `test_toast_visible_before_deadline` | TC-001 mount → auto-dismiss at duration |
| `test_pause_freezes_countdown` / `test_resume_continues_from_remaining` | TC-004 pause-on-hover resumes from remaining |
| `test_manual_close_cancels_timer` | TC-005 X cancels the pending timer |
| `test_action_callback_fires_once` / `test_action_count_starts_at_zero` | TC-006 action fires exactly once |
| `test_dead_click_after_dismiss_does_nothing` | Edge table — click at/after dismiss boundary |
| `test_dismissed_toast_is_fully_removed` | TC-010 removal, not just hidden |
| `test_persistent_toast_never_auto_dismisses` | TC-011 `duration: 0` contract |
| `test_timer_drift_within_tolerance` | TC-012 ±200ms window |
| `test_stack_never_exceeds_max` | TC-013 max-visible invariant under burst |
| `test_queue_drains_fifo` / `test_dequeue_only_on_vacancy` | TC-024 sequential queue semantics |
| `test_dedup_resets_timer` | TC-017 identical message resets the timer |
| `test_priority_preempts_lowest` / `test_low_priority_queues_when_full` | TC-025 priority rules on a full stack |
| `test_paused_toast_does_not_expire` | Hover/focus pause edge |
| `test_no_duplicates_from_retry_burst` | TC-030 storm absorption |
| `test_multiple_dismissals_safe` | Idempotent close (double-dismiss hygiene) |

## Layout

- `toast_lifecycle.py` — `ToastManager`/`Toast`/`State` (~100 lines, stdlib only).
- `tests/test_toast_lifecycle.py` — 20 tests mapped to the resource's TC numbers.
