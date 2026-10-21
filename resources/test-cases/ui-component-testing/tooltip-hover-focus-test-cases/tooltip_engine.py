"""Stdlib model of the tooltip lifecycle used in the tooltip test-cases article.

Models the FormPilot contract: showDelay=500ms, hideDelay=300ms, position=auto,
Escape/scroll/unmount as instant exits, and WCAG 2.2 SC 1.4.13 persistence.
All times are virtual milliseconds driven through ``tick()`` — no real clock.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence


class State(Enum):
    HIDDEN = "hidden"
    SHOW_PENDING = "show_pending"
    VISIBLE = "visible"
    HIDE_PENDING = "hide_pending"


class Side(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"


DEFAULT_FLIP_ORDER = (Side.TOP, Side.BOTTOM, Side.LEFT, Side.RIGHT)


@dataclass(frozen=True)
class Rect:
    """Axis-aligned box in viewport coordinates."""

    x: float
    y: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height


@dataclass(frozen=True)
class Placement:
    """Resolved side plus the tooltip's absolute position in the viewport."""

    side: Side
    x: float
    y: float
    fits: bool


class TooltipController:
    """Virtual-clock state machine for a single tooltip trigger.

    Transitions follow the article's contract: show/hide delays schedule the
    mount/unmount, Escape and trigger removal are instant exits, and Escape
    suppresses re-show until the pointer leaves or the trigger is refocused.
    """

    def __init__(
        self,
        show_delay_ms: int = 500,
        hide_delay_ms: int = 300,
        content: str = "",
    ) -> None:
        self.show_delay_ms = show_delay_ms
        self.hide_delay_ms = hide_delay_ms
        self.content = content
        self.state = State.HIDDEN
        self._pending_at: Optional[int] = None
        self._suppress_until_retrigger = False

    # --- events ---------------------------------------------------------

    def pointer_enter(self, now: int) -> None:
        if self.state == State.HIDE_PENDING:
            self.state = State.VISIBLE  # cancel pending hide (TC-013/TC-022)
        elif self.state == State.HIDDEN and not self._suppress_until_retrigger:
            if not self.content:
                return  # TC-016: empty content mounts nothing
            self.state = State.SHOW_PENDING
            self._pending_at = now + self.show_delay_ms

    def pointer_leave(self, now: int) -> None:
        self._suppress_until_retrigger = False
        if self.state == State.SHOW_PENDING:
            self.state = State.HIDDEN  # transit hover never mounts
            self._pending_at = None
        elif self.state == State.VISIBLE:
            self.state = State.HIDE_PENDING
            self._pending_at = now + self.hide_delay_ms

    def focus(self, now: int) -> None:
        self._suppress_until_retrigger = False
        if self.state == State.HIDDEN and self.content:
            self.state = State.SHOW_PENDING
            self._pending_at = now + self.show_delay_ms

    def blur(self, now: int) -> None:
        if self.state == State.SHOW_PENDING:
            self.state = State.HIDDEN
            self._pending_at = None
        elif self.state in (State.VISIBLE, State.HIDE_PENDING):
            self.state = State.HIDE_PENDING
            self._pending_at = now + self.hide_delay_ms

    def escape(self, now: int) -> None:
        """Instant exit; re-show suppressed until pointer leaves (TC-007)."""
        if self.state != State.HIDDEN:
            self.state = State.HIDDEN
            self._pending_at = None
            self._suppress_until_retrigger = True

    def scroll(self, now: int) -> None:
        self._instant_exit()

    def trigger_unmounted(self, now: int) -> None:
        self._instant_exit()

    def _instant_exit(self) -> None:
        self.state = State.HIDDEN
        self._pending_at = None

    # --- clock ----------------------------------------------------------

    def tick(self, now: int) -> None:
        """Advance the virtual clock; resolves pending timers."""
        if self._pending_at is not None and now >= self._pending_at:
            if self.state == State.SHOW_PENDING:
                self.state = State.VISIBLE
            elif self.state == State.HIDE_PENDING:
                self.state = State.HIDDEN
            self._pending_at = None

    def is_visible(self, now: int) -> bool:
        self.tick(now)
        return self.state == State.VISIBLE


# --- positioning ---------------------------------------------------------


def _coords(trigger: Rect, tip_w: float, tip_h: float, side: Side, gap: float) -> tuple[float, float]:
    cx = trigger.x + trigger.width / 2
    cy = trigger.y + trigger.height / 2
    if side == Side.TOP:
        return cx - tip_w / 2, trigger.y - gap - tip_h
    if side == Side.BOTTOM:
        return cx - tip_w / 2, trigger.bottom + gap
    if side == Side.LEFT:
        return trigger.x - gap - tip_w, cy - tip_h / 2
    return trigger.right + gap, cy - tip_h / 2


def _fits(x: float, y: float, w: float, h: float, viewport: Rect) -> bool:
    return (
        x >= viewport.x
        and y >= viewport.y
        and x + w <= viewport.right
        and y + h <= viewport.bottom
    )


def resolve_position(
    trigger: Rect,
    tip_width: float,
    tip_height: float,
    viewport: Rect,
    preferred: Side = Side.TOP,
    order: Sequence[Side] = DEFAULT_FLIP_ORDER,
    gap: float = 4.0,
) -> Placement:
    """Try ``preferred`` then the flip order; return the first side that fits.

    If nothing fits, falls back to the preferred side clamped inside the
    viewport (the "shift" behavior of Floating UI / Popper).
    """
    sides = [preferred, *[s for s in order if s != preferred]]
    for side in sides:
        x, y = _coords(trigger, tip_width, tip_height, side, gap)
        if _fits(x, y, tip_width, tip_height, viewport):
            return Placement(side=side, x=x, y=y, fits=True)
    x, y = _coords(trigger, tip_width, tip_height, preferred, gap)
    x = min(max(x, viewport.x), viewport.right - tip_width)
    y = min(max(y, viewport.y), viewport.bottom - tip_height)
    return Placement(side=preferred, x=x, y=y, fits=False)


# --- ARIA contract --------------------------------------------------------


def check_aria_contract(trigger_attrs: dict, tip_attrs: dict) -> list[str]:
    """Validate the trigger/tooltip wiring; returns a list of violations."""
    errors: list[str] = []
    describedby = trigger_attrs.get("aria-describedby")
    if not describedby:
        errors.append("trigger has no aria-describedby")
    elif describedby != tip_attrs.get("id"):
        errors.append(f"aria-describedby '{describedby}' does not match tooltip id '{tip_attrs.get('id')}'")
    if tip_attrs.get("role") != "tooltip":
        errors.append("tooltip node is missing role=\"tooltip\"")
    if not trigger_attrs.get("accessible_name"):
        errors.append("trigger has no accessible name")
    return errors
