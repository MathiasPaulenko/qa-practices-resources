"""Executable subset of search-autocomplete-suggestion-test-cases.

Each test names the article case it covers (TC-XX) or the edge-table row.
Runs fully on the virtual clock — no real sleeps, deterministic ordering.
"""

import pytest

from autocomplete_engine import ApiError, SuggestionEngine, dedup, highlight


def fetch_ok(payload, latency=100):
    def fetch(query):
        return payload.get(query, []), latency
    return fetch


def engine_with(payload, latency=100, **kw):
    return SuggestionEngine(fetch_ok(payload, latency), **kw)


def type_and_settle(engine, text, step=50):
    """Type one char per logical event, then let the debounce + API resolve."""
    for ch in text:
        engine.keystroke(ch)
        engine.advance(step)
    engine.advance(1000)


# --- debounce and gates ----------------------------------------------------

def test_debounce_collapses_burst_into_one_request(engine_payload):
    """TC-02: three keystrokes inside the window produce exactly one call."""
    e = engine_payload
    type_and_settle(e, "app")
    assert e.requests == ["app"]
    assert e.rendered == ["apple", "application"]


def test_boundary_keystroke_at_300ms_fires_once(engine_payload):
    """Edge table: a pause of exactly debounce_ms fires; then a new window opens."""
    e = engine_payload
    e.keystroke("app")
    e.advance(299)
    assert e.requests == []           # still inside the window
    e.advance(1)
    assert e.requests == ["app"]      # boundary crossed — fired exactly once


def test_min_length_gate_blocks_short_queries(engine_payload):
    """TC-14 + edge row: 2 chars with min 3 fire nothing; the 3rd unlocks."""
    e = engine_payload
    e.keystroke("ap")
    e.advance(1000)
    assert e.requests == []
    assert e.status == "gated"
    e.keystroke("p")
    e.advance(1000)
    assert e.requests == ["app"]


def test_paste_is_a_single_input_event(engine_payload):
    """Edge table: a 50-char paste must trigger one debounced request."""
    e = engine_payload
    pasted = "apple pie with cinnamon and sugar and more words here"
    e.keystroke(pasted)
    e.advance(1000)
    assert e.requests == [pasted]
    assert len(e.requests) == 1


# --- cache ------------------------------------------------------------------

def test_repeat_query_served_from_cache(engine_payload):
    """TC-07: identical query within TTL = zero new requests."""
    e = engine_payload
    type_and_settle(e, "app")
    e.clear()
    type_and_settle(e, "app")
    assert e.requests == ["app"]      # second lookup never hit the network
    assert e.rendered == ["apple", "application"]


def test_expired_cache_entry_refetches(engine_payload):
    """TC-16 + edge row: TTL+1ms means a fresh request, not stale data."""
    e = engine_payload
    type_and_settle(e, "app")
    e.clear()
    e.advance(60_001)                 # past the 60s TTL
    type_and_settle(e, "app")
    assert e.requests == ["app", "app"]


# --- ordering and failures ---------------------------------------------------

def test_out_of_order_responses_latest_wins():
    """TC-11 + edge row: the slow first query never paints over the second."""
    def fetch(q):
        return (["aaa"], 600) if q == "aaa" else (["apple"], 50)
    e = SuggestionEngine(fetch, min_length=1)
    e.keystroke("aaa")
    e.advance(400)                    # first request fires (slow)
    e.query = "apple"                 # user kept typing — new pending query
    e._deadline = e.now               # force the second debounce to fire now
    e.advance(1000)
    assert e.rendered == ["apple"]    # late "aaa" response was discarded


def test_api_error_surfaces_error_state():
    """TC-12: a failing API lands on 'error', and the next keystroke retries."""
    calls = []

    def flaky(q):
        calls.append(q)
        if len(calls) == 1:
            raise ApiError("HTTP 500")
        return ["apple"], 50

    e = SuggestionEngine(flaky)
    e.keystroke("app")
    e.advance(400)
    assert e.status == "error"
    assert e.requests == ["app"]
    e.keystroke("le")                 # user keeps typing — retry
    e.advance(1000)
    assert e.rendered == ["apple"]
    assert e.requests == ["app", "apple"]


def test_slow_response_keeps_loading_then_renders(engine_payload):
    """TC-13: pending state while waiting; later response renders."""
    e = engine_payload
    e.keystroke("app")
    e.advance(300)                    # debounce fires, request in flight
    assert e.status == "loading"
    e.advance(200)                    # latency elapses
    assert e.status == "open"


# --- rendering ---------------------------------------------------------------

def test_no_results_sets_empty_status(engine_payload):
    """TC-08: zero matches must produce an explicit empty state."""
    e = engine_payload
    type_and_settle(e, "xyz")
    assert e.status == "empty"
    assert e.rendered == []


def test_duplicates_are_collapsed(engine_payload):
    """TC-18: 'apple' and 'apple ' (whitespace variant) render once."""
    e = SuggestionEngine(lambda q: (["apple", "apple", "apple "], 50))
    type_and_settle(e, "app")
    assert e.rendered == ["apple"]
    assert dedup(["a ", "a", " b"]) == ["a", "b"]


def test_render_capped_at_max_items():
    """Edge table: 11 items in the payload, UI cap of 10 — exactly 10 render."""
    e = SuggestionEngine(lambda q: ([f"item{i}" for i in range(11)], 50), max_items=10)
    type_and_settle(e, "app")
    assert len(e.rendered) == 10


def test_highlight_wraps_matched_substring():
    """TC-06: the typed substring is wrapped in <mark>, unmatched text is plain."""
    assert highlight("apple", "app") == "<mark>app</mark>le"
    assert highlight("Red Apple", "apple") == "Red <mark>Apple</mark>"
    assert highlight("cherry", "app") == "cherry"          # no match, no mark
    assert highlight("apple", "") == "apple"               # empty query, no mark


# --- interaction ------------------------------------------------------------

def test_recents_surface_on_empty_focus_and_dedup():
    """TC-09: recents show on empty focus; selecting re-records most-recent-first."""
    e = engine_with({"app": ["apple"]})
    e.recents = ["banana", "orange"]
    assert e.focus() == "open"
    assert e.rendered == ["banana", "orange"]
    e.select("banana")
    assert e.recents[0] == "banana"   # moved to front, not duplicated
    assert len(e.recents) == 2


def test_escape_closes_dropdown_but_keeps_query(engine_payload):
    """TC-05: Escape dismisses the list; the input text survives."""
    e = engine_payload
    type_and_settle(e, "app")
    e.escape()
    assert e.rendered == []
    assert e.query == "app"


def test_clear_resets_input_and_pending_debounce(engine_payload):
    """TC-26: clear empties the field and cancels any pending request."""
    e = engine_payload
    e.keystroke("apx")
    e.clear()
    assert e.query == ""
    e.advance(1000)
    assert e.requests == []           # pending debounce was cancelled


@pytest.fixture
def engine_payload():
    return SuggestionEngine(fetch_ok({"app": ["apple", "application"], "xyz": []}))
