"""Minimal skeleton-loader state machine mirroring the resource's contract.

Lifecycle (matches the resource diagram):
    IDLE -> mount() -> LOADING (shimmer unless reduced-motion, aria-busy=true,
    min display floor) -> resolve() -> CONTENT | ERROR | TIMEOUT
    ERROR/TIMEOUT -> retry() -> LOADING

Every exit from LOADING must resolve exactly once: shimmer stops and
aria-busy clears on success *and* failure — a skeleton without an error
path is the bug this lab exists to catch.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class State(Enum):
    """Skeleton view states."""

    IDLE = "idle"
    LOADING = "loading"
    CONTENT = "content"
    ERROR = "error"
    TIMEOUT = "timeout"


@dataclass
class SkeletonView:
    """A skeleton placeholder over one content region."""

    min_display_ms: int = 300
    reduced_motion: bool = False
    state: State = State.IDLE
    aria_busy: bool = False
    shimmer_active: bool = False
    mounted_ms: int = 0
    displayed_ms: int = 0
    retries: int = 0
    events: list[dict] = field(default_factory=list)

    def mount(self, at_ms: int = 0) -> None:
        """Show the skeleton. Reduced motion suppresses the shimmer only."""
        self.state = State.LOADING
        self.mounted_ms = at_ms
        self.aria_busy = True
        self.shimmer_active = not self.reduced_motion

    def resolve(self, outcome: str, at_ms: int) -> int:
        """Resolve LOADING once; returns the actual display duration in ms."""
        if self.state is not State.LOADING:
            raise RuntimeError(f"cannot resolve from {self.state.value}")
        exit_ms = max(at_ms, self.mounted_ms + self.min_display_ms)
        self.displayed_ms = exit_ms - self.mounted_ms
        self.shimmer_active = False
        self.aria_busy = False
        self.state = {
            "success": State.CONTENT,
            "error": State.ERROR,
            "timeout": State.TIMEOUT,
        }[outcome]
        self.events.append(
            {
                "event": "skeleton_display_time",
                "component": "project-grid",
                "ms": self.displayed_ms,
            }
        )
        return self.displayed_ms

    def retry(self, at_ms: int) -> None:
        """ERROR/TIMEOUT may re-mount exactly once per retry."""
        if self.state not in (State.ERROR, State.TIMEOUT):
            raise RuntimeError(f"cannot retry from {self.state.value}")
        self.retries += 1
        self.mount(at_ms)


def check_layout_match(
    skeleton_boxes: list[tuple[float, float, float, float]],
    content_boxes: list[tuple[float, float, float, float]],
    tolerance_px: float = 2.0,
) -> bool:
    """Every skeleton box (x, y, w, h) must match its content box within tolerance."""
    if len(skeleton_boxes) != len(content_boxes):
        return False
    return all(
        all(abs(s - c) <= tolerance_px for s, c in zip(sbox, cbox))
        for sbox, cbox in zip(skeleton_boxes, content_boxes)
    )


def aria_issues(view: SkeletonView, shapes_aria_hidden: bool) -> list[str]:
    """Return ARIA contract violations for the current view state."""
    issues = []
    if view.state is State.LOADING:
        if not view.aria_busy:
            issues.append("aria-busy missing while loading")
        if not shapes_aria_hidden:
            issues.append("decorative shapes not hidden from AT")
    elif view.aria_busy:
        issues.append("aria-busy stuck true after exit")
    return issues
