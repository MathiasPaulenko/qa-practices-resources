"""Executable subset of the tooltip test cases, driven on a virtual clock."""

import pytest

from tooltip_engine import (
    Rect,
    Side,
    State,
    TooltipController,
    check_aria_contract,
    resolve_position,
)

VIEWPORT = Rect(0, 0, 1280, 768)


# --- lifecycle (TC-001, TC-002, boundary rows 1-2) -------------------------


def test_show_delay_gates_the_mount():
    tip = TooltipController(show_delay_ms=500, content="help")
    tip.pointer_enter(0)
    tip.tick(300)
    assert tip.state == State.SHOW_PENDING  # TC-002: nothing at 300ms
    tip.tick(600)
    assert tip.state == State.VISIBLE


def test_transit_hover_never_mounts():
    tip = TooltipController(show_delay_ms=500, content="help")
    tip.pointer_enter(0)
    tip.pointer_leave(150)  # swept across in 150ms < 500ms
    tip.tick(2000)
    assert tip.state == State.HIDDEN


def test_pointer_into_tooltip_cancels_pending_hide():
    tip = TooltipController(content="with a link")
    tip.pointer_enter(0)
    tip.tick(600)
    tip.pointer_leave(1000)  # hide pending until 1300
    tip.pointer_enter(1200)  # crosses the gap inside the window
    tip.tick(2000)
    assert tip.state == State.VISIBLE  # WCAG hoverable: still open


def test_escape_suppresses_reshow_until_retrigger():
    tip = TooltipController(content="help")
    tip.pointer_enter(0)
    tip.tick(600)
    tip.escape(700)
    assert tip.state == State.HIDDEN
    tip.pointer_enter(800)  # pointer never left — suppressed
    tip.tick(2000)
    assert tip.state == State.HIDDEN
    tip.pointer_leave(2100)
    tip.pointer_enter(2200)  # fresh enter re-arms the delay
    tip.tick(2800)
    assert tip.state == State.VISIBLE


def test_focus_blur_parity_with_hover():
    tip = TooltipController(content="help")
    tip.focus(0)
    tip.tick(600)
    assert tip.state == State.VISIBLE  # same contract as hover
    tip.blur(1000)
    tip.tick(1350)  # hideDelay=300
    assert tip.state == State.HIDDEN


def test_instant_exits_skip_the_hide_delay():
    for event in ("scroll", "trigger_unmounted"):
        tip = TooltipController(content="help")
        tip.pointer_enter(0)
        tip.tick(600)
        getattr(tip, event)(700)
        assert tip.state == State.HIDDEN, event


def test_empty_content_mounts_nothing():
    tip = TooltipController(content="")
    tip.pointer_enter(0)
    tip.focus(0)
    tip.tick(2000)
    assert tip.state == State.HIDDEN


def test_tooltip_stays_visible_during_sustained_hover():
    tip = TooltipController(content="help")
    tip.pointer_enter(0)
    tip.tick(30_000)  # 30s dwell — persistent per WCAG 1.4.13
    assert tip.state == State.VISIBLE


# --- positioning (TC-011, TC-012, TC-024) -----------------------------------

TRIGGER = Rect(620, 360, 40, 24)  # centered in a 1280x768 viewport


def test_auto_flip_top_to_bottom_at_top_edge():
    near_top = Rect(620, 8, 40, 24)
    p = resolve_position(near_top, 200, 48, VIEWPORT)
    assert p.side == Side.BOTTOM and p.fits


def test_auto_flip_right_to_left_at_right_edge():
    near_right = Rect(1260, 360, 16, 24)
    p = resolve_position(near_right, 200, 48, VIEWPORT, preferred=Side.RIGHT)
    assert p.side == Side.LEFT and p.fits


def test_preferred_side_wins_when_it_fits():
    p = resolve_position(TRIGGER, 200, 48, VIEWPORT)
    assert p.side == Side.TOP and p.fits


def test_no_side_fits_clamps_inside_viewport():
    huge_tip = (TRIGGER, 700, 400, VIEWPORT)
    p = resolve_position(*huge_tip)
    assert not p.fits  # clamped fallback, never negative coords
    assert p.x >= 0 and p.y >= 0


# --- ARIA contract (TC-021, TC-016, boundary row 5) -------------------------


def test_aria_contract_valid_wiring():
    errors = check_aria_contract(
        {"aria-describedby": "fp-tip-1", "accessible_name": "Field help"},
        {"id": "fp-tip-1", "role": "tooltip"},
    )
    assert errors == []


def test_aria_contract_catches_dangling_describedby():
    errors = check_aria_contract(
        {"aria-describedby": "fp-tip-404", "accessible_name": "Field help"},
        {"id": "fp-tip-1", "role": "tooltip"},
    )
    assert any("does not match" in e for e in errors)
