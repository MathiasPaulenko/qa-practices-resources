"""Pytest suite for the skeleton lifecycle, mapped to the resource's TCs."""

import pytest

from skeleton_states import SkeletonView, State, aria_issues, check_layout_match


@pytest.fixture
def view():
    return SkeletonView(min_display_ms=300)


# TC-007/013/014 — every outcome exits LOADING exactly once
def test_skeleton_never_stays_loading(view):
    expected = {"success": State.CONTENT, "error": State.ERROR, "timeout": State.TIMEOUT}
    for outcome, state in expected.items():
        v = SkeletonView(min_display_ms=300)
        v.mount()
        v.resolve(outcome, at_ms=500)
        assert v.state == state


# TC-009/TC-016 — minimum display time prevents a flash
def test_min_display_time_holds(view):
    view.mount(at_ms=0)
    shown = view.resolve("success", at_ms=120)  # data arrives early
    assert shown == 300  # held to the floor, not 120


def test_slow_load_shows_natural_duration(view):
    view.mount(at_ms=0)
    shown = view.resolve("success", at_ms=1500)
    assert shown == 1500


# TC-002 — shimmer runs while loading
def test_shimmer_runs_while_loading(view):
    view.mount()
    assert view.shimmer_active is True


# TC-022 — reduced motion disables the shimmer, keeps the placeholder
def test_reduced_motion_disables_shimmer():
    v = SkeletonView(reduced_motion=True)
    v.mount()
    assert v.state is State.LOADING
    assert v.shimmer_active is False
    assert v.aria_busy is True  # loading semantics survive


# TC-013 — content exit: one swap, shimmer off, busy cleared
def test_content_exit_is_single_clean_swap(view):
    view.mount()
    view.resolve("success", at_ms=800)
    assert view.state is State.CONTENT
    assert view.shimmer_active is False
    assert view.aria_busy is False
    with pytest.raises(RuntimeError):
        view.resolve("success", at_ms=900)  # no double swap


# TC-007 — error path exits to ERROR, not infinite shimmer
def test_error_exit_sets_aria_busy_false(view):
    view.mount()
    view.resolve("error", at_ms=2000)
    assert view.state is State.ERROR
    assert view.shimmer_active is False
    assert view.aria_busy is False


# TC-014 — timeout reaches a distinct retryable state
def test_timeout_exit_is_retryable(view):
    view.mount()
    view.resolve("timeout", at_ms=15000)
    assert view.state is State.TIMEOUT
    view.retry(at_ms=16000)
    assert view.state is State.LOADING
    assert view.retries == 1


def test_retry_restores_shimmer_and_busy(view):
    view.mount()
    view.resolve("error", at_ms=500)
    view.retry(at_ms=600)
    assert view.shimmer_active is True
    assert view.aria_busy is True


def test_no_retry_from_content(view):
    view.mount()
    view.resolve("success", at_ms=500)
    with pytest.raises(RuntimeError):
        view.retry(at_ms=600)


# TC-028 — one display-time event per resolution
def test_analytics_event_fires_once(view):
    view.mount()
    view.resolve("success", at_ms=800)
    assert view.events == [
        {"event": "skeleton_display_time", "component": "project-grid", "ms": 800}
    ]


# TC-001/TC-011 — layout matching within ±2px, count must match
CARD = [(40, 16, 40, 40), (92, 20, 180, 18), (92, 44, 180, 12), (92, 60, 120, 12)]


def test_layout_match_within_tolerance():
    content = [(40, 16, 40, 40), (92, 20, 180, 18), (91, 45, 180, 12), (92, 61, 121, 12)]
    assert check_layout_match(CARD, content, tolerance_px=2) is True


def test_layout_match_rejects_drift():
    drifted = [(40, 16, 40, 40), (92, 20, 180, 18), (92, 44, 180, 12), (92, 100, 120, 12)]
    assert check_layout_match(CARD, drifted, tolerance_px=2) is False


def test_layout_match_rejects_count_mismatch():
    assert check_layout_match(CARD, CARD[:3], tolerance_px=2) is False


# TC-021 — ARIA contract while loading and after exit
def test_aria_contract_while_loading(view):
    view.mount()
    assert aria_issues(view, shapes_aria_hidden=True) == []
    assert "decorative shapes not hidden from AT" in aria_issues(
        view, shapes_aria_hidden=False
    )


def test_aria_contract_after_exit(view):
    view.mount()
    view.resolve("success", at_ms=500)
    assert aria_issues(view, shapes_aria_hidden=True) == []
    # a buggy view that kept aria-busy=true would be caught here
    view.aria_busy = True
    assert "aria-busy stuck true after exit" in aria_issues(
        view, shapes_aria_hidden=True
    )
