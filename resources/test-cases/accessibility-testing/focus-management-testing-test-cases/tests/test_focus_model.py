"""Pytest suite for the focus-order contract model.

Each test maps to a test case in the "Focus Management Test Cases"
resource on QAPractices.com (TC-001 .. TC-015).
"""

import pytest

from focus_model import Focusable, FocusModelError, Page


def page_of(*keys: str) -> Page:
    return Page(list(keys))


# ---------------------------------------------------------------- TC-001 tab order

def test_tab_visits_elements_in_dom_order():
    page = page_of("nav", "filter", "action", "row-1", "row-2")
    visited = [page.tab() for _ in range(5)]
    assert visited == ["nav", "filter", "action", "row-1", "row-2"]


def test_tab_wraps_to_first_after_last():
    page = page_of("a", "b")
    assert [page.tab() for _ in range(4)] == ["a", "b", "a", "b"]


def test_hidden_elements_are_skipped_in_tab_order():
    page = Page([
        Focusable("a"),
        Focusable("offscreen", hidden=True),
        Focusable("b"),
    ])
    assert page.tab_order() == ["a", "b"]


# ---------------------------------------------------------------- TC-004 skip link

def test_skip_link_moves_focus_to_main():
    page = Page(["skip", "nav-1", "nav-2", "main", "content"], skip_target="main")
    assert page.tab() == "skip"
    assert page.activate_skip_link() == "main"
    # the next Tab after the skip lands on content, not on nav-2
    assert page.tab() == "content"


def test_skip_link_without_target_raises():
    page = page_of("a", "b")
    with pytest.raises(FocusModelError):
        page.activate_skip_link()


# ---------------------------------------------------------------- TC-005 modal trap & return

def test_modal_mounts_initial_focus_inside():
    page = page_of("nav", "trigger", "footer")
    page.script_focus("trigger")
    dlg = page.open_modal(trigger="trigger", controls=["input", "ok"])
    assert page.active_element == "input"
    assert dlg.is_open


def test_modal_traps_tab_cyclically():
    page = page_of("nav", "trigger", "footer")
    page.script_focus("trigger")
    dlg = page.open_modal(trigger="trigger", controls=["input", "ok", "cancel"])
    visited = [dlg.tab() for _ in range(6)]
    # cycles input -> ok -> cancel -> input -> ok -> cancel, never leaves
    assert visited == ["ok", "cancel", "input", "ok", "cancel", "input"]
    assert all(k in dlg.controls for k in visited)


def test_modal_traps_shift_tab_backwards():
    page = page_of("nav", "trigger", "footer")
    page.script_focus("trigger")
    dlg = page.open_modal(trigger="trigger", controls=["input", "ok", "cancel"])
    assert dlg.shift_tab() == "cancel"  # wraps to last
    assert dlg.shift_tab() == "ok"


def test_modal_never_leaks_to_page_behind():
    page = page_of("nav", "trigger", "footer")
    page.script_focus("trigger")
    dlg = page.open_modal(trigger="trigger", controls=["input", "ok"])
    for _ in range(12):
        dlg.tab()
    assert page.active_element in dlg.controls
    assert page.active_element not in ("nav", "footer")


def test_escape_restores_focus_to_trigger():
    page = page_of("nav", "trigger", "footer")
    dlg = page.open_modal(trigger="trigger", controls=["input", "ok"])
    dlg.escape()
    assert page.active_element == "trigger"
    assert not dlg.is_open


def test_close_button_restores_focus_to_trigger():
    page = page_of("nav", "trigger", "footer")
    dlg = page.open_modal(trigger="trigger", controls=["input", "ok"])
    assert dlg.close_via_button() == "trigger"


def test_tab_on_closed_modal_raises():
    page = page_of("nav", "trigger", "footer")
    dlg = page.open_modal(trigger="trigger", controls=["input"])
    dlg.escape()
    with pytest.raises(FocusModelError):
        dlg.tab()


def test_modal_without_controls_raises():
    page = page_of("nav", "trigger", "footer")
    with pytest.raises(FocusModelError):
        page.open_modal(trigger="trigger", controls=[])


# ---------------------------------------------------------------- TC-007 positive tabindex

def test_positive_tabindex_is_detected():
    page = Page([Focusable("a"), Focusable("cheat", tabindex=1), Focusable("b")])
    assert page.has_positive_tabindex()
    assert page.positive_tabindex_keys() == ["cheat"]


def test_positive_tabindex_hijacks_dom_order():
    page = Page([
        Focusable("nav"),
        Focusable("card", tabindex=1),
        Focusable("filter"),
    ])
    # browser visits positive tabindex first — this is the bug TC-007 flags
    assert page.tab_order() == ["card", "nav", "filter"]


def test_multiple_positive_values_sort_ascending():
    page = Page([
        Focusable("a"),
        Focusable("p2", tabindex=2),
        Focusable("p1", tabindex=1),
        Focusable("b"),
    ])
    assert page.tab_order() == ["p1", "p2", "a", "b"]


# ---------------------------------------------------------------- TC-010 reverse order

def test_shift_tab_retraces_forward_sequence():
    page = page_of("a", "b", "c", "d")
    fwd = [page.tab() for _ in range(4)]
    bwd = [page.shift_tab() for _ in range(4)]
    # from the last element, backward walks the same path reversed and wraps to it
    assert bwd == list(reversed(fwd[:-1])) + [fwd[-1]]


# ---------------------------------------------------------------- TC-012 dynamic removal

def test_removed_focused_node_lands_on_fallback():
    page = page_of("list", "item-1", "item-2")
    page.script_focus("item-1")
    assert page.remove_focused(fallback="list") == "list"


def test_removed_node_without_fallback_drops_to_body():
    page = page_of("list", "item-1")
    page.script_focus("item-1")
    # the bug contract: browser default is body — the fix is a fallback
    assert page.remove_focused() == "body"


def test_removed_node_leaves_tab_order():
    page = page_of("a", "item-1", "b")
    page.script_focus("item-1")
    page.remove_focused(fallback="a")
    assert page.tab_order() == ["a", "b"]


# ---------------------------------------------------------------- TC-014 tabindex=-1

def test_minus_one_is_absent_from_tab_order():
    page = Page([
        Focusable("a"),
        Focusable("dialog-root", tabindex=-1),
        Focusable("b"),
    ])
    assert page.tab_order() == ["a", "b"]


def test_minus_one_is_script_focusable():
    page = Page([Focusable("a"), Focusable("dialog-root", tabindex=-1)])
    assert page.script_focus("dialog-root") == "dialog-root"


def test_script_focus_on_removed_node_raises():
    page = page_of("a", "gone")
    page.script_focus("gone")
    page.remove_focused()
    with pytest.raises(FocusModelError):
        page.script_focus("gone")
