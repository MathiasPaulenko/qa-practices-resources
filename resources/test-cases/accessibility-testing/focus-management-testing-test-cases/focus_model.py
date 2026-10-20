"""Focus-order contract model for keyboard focus management testing.

A stdlib-only simulation of the DOM focus contract described in the
"Focus Management Test Cases" resource on QAPractices.com:

- Tab order follows DOM order for tabindex=0 elements.
- Positive tabindex values are visited first, sorted ascending —
  this is why a single tabindex="1" silently hijacks the page order.
- tabindex="-1" elements are script-focusable but never in Tab order.
- A modal traps Tab/Shift+Tab cyclically and returns focus to its
  trigger on close.
- Removing a focused node must land focus on a defined fallback,
  never silently on document.body.

The model is intentionally small: it encodes the *contract* so tests
can assert behavior without a browser. Real-world verification uses
Playwright + document.activeElement, as shown in the resource.
"""

from __future__ import annotations

from dataclasses import dataclass, field


class FocusModelError(Exception):
    """Raised when the focus contract is violated."""


@dataclass
class Focusable:
    """A single focusable element in the page model."""

    key: str
    tabindex: int = 0
    hidden: bool = False
    removed: bool = False

    @property
    def in_tab_order(self) -> bool:
        return self.tabindex >= 0 and not self.hidden and not self.removed


class Modal:
    """A dialog that traps focus cyclically until closed."""

    def __init__(self, page: "Page", trigger: str, controls: list[str]) -> None:
        self.page = page
        self.trigger = trigger
        self.controls = controls
        self.is_open = True
        if not controls:
            raise FocusModelError("a modal needs at least one control to focus")
        page.active_element = controls[0]  # initial focus mounts inside

    def tab(self) -> str:
        """Cycle focus forward inside the modal; wraps to the first control."""
        if not self.is_open:
            raise FocusModelError("tab on a closed modal")
        idx = self.controls.index(self.page.active_element)
        self.page.active_element = self.controls[(idx + 1) % len(self.controls)]
        return self.page.active_element

    def shift_tab(self) -> str:
        """Cycle focus backward inside the modal; wraps to the last control."""
        if not self.is_open:
            raise FocusModelError("shift+tab on a closed modal")
        idx = self.controls.index(self.page.active_element)
        self.page.active_element = self.controls[(idx - 1) % len(self.controls)]
        return self.page.active_element

    def escape(self) -> str:
        """Close the modal and restore focus to the trigger element."""
        self.is_open = False
        self.page.active_element = self.trigger
        return self.page.active_element

    def close_via_button(self) -> str:
        """Close via a click-equivalent action; also restores the trigger."""
        return self.escape()


@dataclass
class Page:
    """A page holding an ordered DOM of focusable keys."""

    focusables: list[Focusable] = field(default_factory=list)
    active_element: str = "body"
    skip_target: str | None = None

    def __init__(self, focusables: list[str | Focusable], skip_target: str | None = None) -> None:
        self.focusables = [
            f if isinstance(f, Focusable) else Focusable(key=f) for f in focusables
        ]
        self.active_element = "body"
        self.skip_target = skip_target

    def _lookup(self, key: str) -> Focusable | None:
        return next((f for f in self.focusables if f.key == key), None)

    def tab_order(self) -> list[str]:
        """Browser tab order: positive tabindex first (ascending), then DOM order."""
        order = [f for f in self.focusables if f.in_tab_order]
        positive = sorted((f for f in order if f.tabindex > 0), key=lambda f: f.tabindex)
        natural = [f for f in order if f.tabindex == 0]
        return [f.key for f in positive + natural]

    def has_positive_tabindex(self) -> bool:
        return any(f.tabindex > 0 for f in self.focusables)

    def positive_tabindex_keys(self) -> list[str]:
        return [f.key for f in self.focusables if f.tabindex > 0]

    def tab(self) -> str:
        order = self.tab_order()
        if self.active_element not in order:
            self.active_element = order[0]
        else:
            idx = order.index(self.active_element)
            self.active_element = order[(idx + 1) % len(order)]
        return self.active_element

    def shift_tab(self) -> str:
        order = self.tab_order()
        if self.active_element not in order:
            self.active_element = order[-1]
        else:
            idx = order.index(self.active_element)
            self.active_element = order[(idx - 1) % len(order)]
        return self.active_element

    def script_focus(self, key: str) -> str:
        """.focus() — works on tabindex=-1 and 0 elements, not on removed ones."""
        f = self._lookup(key)
        if f is None or f.removed:
            raise FocusModelError(f"cannot focus {key!r}: not in the DOM")
        self.active_element = key
        return key

    def activate_skip_link(self) -> str:
        """The skip link moves focus to the main landmark."""
        if self.skip_target is None:
            raise FocusModelError("no skip link target configured")
        return self.script_focus(self.skip_target)

    def open_modal(self, trigger: str, controls: list[str]) -> Modal:
        """Open a modal from a trigger element; focus mounts inside."""
        if self.active_element != trigger:
            self.script_focus(trigger)
        return Modal(self, trigger, controls)

    def remove_focused(self, fallback: str | None = None) -> str:
        """Remove the focused node; focus lands on fallback or drops to body.

        Real browsers send focus to document.body when a focused node is
        removed. The contract asks for a deliberate fallback — passing
        `fallback` models the fix; omitting it models the bug.
        """
        f = self._lookup(self.active_element)
        if f is not None:
            f.removed = True
        self.active_element = fallback if fallback is not None else "body"
        return self.active_element
