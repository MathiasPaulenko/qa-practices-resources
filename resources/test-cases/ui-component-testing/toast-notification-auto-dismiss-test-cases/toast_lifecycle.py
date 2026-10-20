"""Toast notification lifecycle state machine.

Mirrors the contracts exercised in the toast test-cases resource:
auto-dismiss timing, pause-on-hover resume-from-remaining, manual
close cancelling the timer, action callbacks firing exactly once,
stacking cap, FIFO queue, dedup and priority preemption.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Optional


class State(Enum):
    VISIBLE = auto()
    PAUSED = auto()
    REMOVED = auto()


@dataclass
class Toast:
    message: str
    priority: int = 0
    duration_ms: int = 5000
    action: Optional[Callable] = None
    persistent: bool = False
    state: State = State.VISIBLE
    remaining_ms: int = 0
    action_count: int = 0

    def __post_init__(self) -> None:
        self.remaining_ms = self.duration_ms


class ToastManager:
    """Manages toast visibility, timers and stacking policies."""

    def __init__(self, duration_ms: int = 5000, max_visible: int = 3,
                 dedup_reset: bool = True) -> None:
        self.duration_ms = duration_ms
        self.max_visible = max_visible
        self.dedup_reset = dedup_reset
        self.visible: list[Toast] = []
        self.queue: list[Toast] = []

    def show(self, message: str, *, priority: int = 0,
             duration_ms: Optional[int] = None,
             action: Optional[Callable] = None,
             persistent: bool = False) -> Toast:
        toast = Toast(
            message,
            priority=priority,
            duration_ms=duration_ms if duration_ms is not None else self.duration_ms,
            action=action,
            persistent=persistent,
        )
        if self.dedup_reset:
            for existing in self.visible:
                if existing.message == message and existing.state == State.VISIBLE:
                    existing.remaining_ms = existing.duration_ms
                    return existing
        if len(self.visible) >= self.max_visible:
            lowest = min(self.visible, key=lambda t: t.priority)
            if toast.priority > lowest.priority:
                self.visible.remove(lowest)
                self.visible.append(toast)
                return toast
            self.queue.append(toast)
            return toast
        self.visible.append(toast)
        return toast

    def tick(self, ms: int) -> None:
        for toast in list(self.visible):
            if toast.state != State.VISIBLE or toast.persistent:
                continue
            toast.remaining_ms -= ms
            if toast.remaining_ms <= 0:
                self._remove(toast)

    def pause(self, toast: Toast) -> None:
        if toast.state == State.VISIBLE:
            toast.state = State.PAUSED

    def resume(self, toast: Toast) -> None:
        if toast.state == State.PAUSED:
            toast.state = State.VISIBLE

    def close(self, toast: Toast) -> None:
        self._remove(toast)

    def click_action(self, toast: Toast) -> bool:
        if toast.state == State.REMOVED or toast not in self.visible:
            return False
        toast.action_count += 1
        if toast.action:
            toast.action()
        self._remove(toast)
        return True

    def _remove(self, toast: Toast) -> None:
        toast.state = State.REMOVED
        if toast in self.visible:
            self.visible.remove(toast)
        while self.queue and len(self.visible) < self.max_visible:
            self.visible.append(self.queue.pop(0))
