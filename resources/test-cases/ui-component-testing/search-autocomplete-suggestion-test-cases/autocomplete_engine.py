"""Stdlib model of a debounced search-autocomplete combobox.

The engine models the client side of a typeahead: a virtual clock (no real
sleeps), a debounce window that resets per keystroke, a minimum-length gate,
a TTL cache, a latest-query-wins guard against out-of-order responses, a
recents list, dedup, render capping and substring highlighting.

`fetch` is injected: ``fetch(query) -> (suggestions, latency_ms)`` and may
raise ``ApiError`` to simulate a failed response.
"""


class ApiError(Exception):
    """Raised by the injected fetch when the suggestions API fails."""


def dedup(items):
    """Collapse duplicate suggestions, ignoring surrounding whitespace.

    Order is preserved; the first occurrence wins.
    """
    seen = set()
    out = []
    for item in items:
        key = item.strip().casefold()
        if key and key not in seen:
            seen.add(key)
            out.append(item.strip())
    return out


def highlight(text, query):
    """Wrap the first case-insensitive occurrence of *query* in <mark>."""
    idx = text.casefold().find(query.casefold())
    if idx < 0 or not query:
        return text
    return text[:idx] + "<mark>" + text[idx:idx + len(query)] + "</mark>" + text[idx + len(query):]


class SuggestionEngine:
    """A deterministic autocomplete client driven by a virtual clock."""

    def __init__(self, fetch, *, min_length=3, debounce_ms=300,
                 cache_ttl_ms=60_000, max_items=10, max_recents=5):
        self._fetch = fetch
        self.min_length = min_length
        self.debounce_ms = debounce_ms
        self.cache_ttl_ms = cache_ttl_ms
        self.max_items = max_items
        self.max_recents = max_recents

        self.now = 0                # virtual clock, milliseconds
        self.query = ""
        self.focused = False
        self.recents = []           # most recent first
        self.requests = []          # audit log: every query sent to the API

        self._deadline = None       # debounce fire time (ms) or None
        self._cache = {}            # query -> (fetched_at_ms, suggestions)
        self._inflight = []         # pending responses, unordered delivery
        self._next_token = 0
        self._latest_token = 0      # latest-query-wins guard

        self.rendered = []          # suggestion strings currently shown
        self.status = "idle"        # idle|gated|debouncing|loading|open|empty|error

    # -- user input ------------------------------------------------------

    def focus(self):
        """Focus the input; an empty query surfaces recent searches."""
        self.focused = True
        if not self.query and self.recents:
            self.rendered = list(self.recents)
            self.status = "open"
        return self.status

    def keystroke(self, text):
        """Append text from one logical input event (key, paste, IME end)."""
        self.query += text
        if len(self.query) < self.min_length:
            self._deadline = None
            self.status = "gated" if self.query else "idle"
            self.rendered = []
            return self.status
        self._deadline = self.now + self.debounce_ms
        self.status = "debouncing"
        return self.status

    def escape(self):
        """Dismiss the dropdown; the typed query is kept."""
        self.rendered = []
        self.status = "idle" if not self.query else "debouncing"
        if self._deadline is not None:
            self.status = "debouncing"
        return self.status

    def clear(self):
        """Clear button: empty input, close dropdown, keep focus."""
        self.query = ""
        self.rendered = []
        self._deadline = None
        self.status = "idle"
        return self.status

    def select(self, suggestion):
        """Pick a suggestion: fill the input, record it in recents."""
        self.query = suggestion
        if suggestion in self.recents:
            self.recents.remove(suggestion)
        self.recents.insert(0, suggestion)
        del self.recents[self.max_recents:]
        self.rendered = []
        self.status = "idle"
        return self.query

    # -- clock ------------------------------------------------------------

    def advance(self, ms):
        """Move the virtual clock; fire due debounces, deliver due responses."""
        target = self.now + ms
        if self._deadline is not None and self._deadline <= target:
            self.now = self._deadline
            self._fire()
        self.now = target
        self._deliver_due()
        return self.now

    # -- internals ---------------------------------------------------------

    def _fire(self):
        q = self.query
        self._deadline = None
        hit = self._cache.get(q)
        if hit and hit[0] + self.cache_ttl_ms > self.now:
            self._render(hit[1])
            return
        self._next_token += 1
        token = self._next_token
        self._latest_token = token
        self.requests.append(q)
        try:
            suggestions, latency = self._fetch(q)
        except ApiError:
            self.status = "error"
            return
        self.status = "loading"
        self._inflight.append({
            "token": token,
            "query": q,
            "deliver_at": self.now + latency,
            "payload": suggestions,
        })

    def _deliver_due(self):
        for resp in sorted(self._inflight, key=lambda r: r["deliver_at"]):
            if resp["deliver_at"] > self.now:
                break
            self._inflight.remove(resp)
            if resp["token"] != self._latest_token:
                continue  # stale response — discarded
            self._cache[resp["query"]] = (self.now, resp["payload"])
            self._render(resp["payload"])

    def _render(self, payload):
        self.rendered = dedup(payload)[:self.max_items]
        self.status = "open" if self.rendered else "empty"
