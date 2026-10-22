# Search Autocomplete Test Cases — Companion

Companion resource for [Search Autocomplete Test Cases: Debounce, Keyboard, ARIA](https://qapractices.com/test-cases/search-autocomplete-suggestion-test-cases/).

## Contents

- `autocomplete_engine.py` — stdlib-only model of a debounced autocomplete client on a virtual clock: minimum-length gate, 300ms debounce window, TTL cache, latest-query-wins guard against out-of-order responses, dedup, render capping, substring highlighting, recents and Escape/clear semantics.
- `autocomplete.html` — static fixture implementing the real ARIA combobox (role/expanded/controls/activedescendant, listbox, options, `aria-live` status, keyboard nav, mark highlighting, localStorage recents) for manual and Playwright verification. Open it in any browser.
- `tests/conftest.py` — puts the engine on `sys.path`.
- `tests/test_autocomplete_engine.py` — executable subset of the article's cases: debounce collapse (TC-02), boundary keystroke at 300ms (edge), paste as one event (edge), min-length gate (TC-14), cache hit (TC-07) and TTL expiry (TC-16), out-of-order latest-wins (TC-11), API error + retry (TC-12), loading state (TC-13), no-results (TC-08), dedup (TC-18), render cap (edge), highlighting (TC-06), recents on empty focus (TC-09), Escape keeps query (TC-05) and clear reset (TC-26).

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Expected output: `16 passed`.

The browser fixture needs no build step: open `autocomplete.html` and type — debounce, cache, stale-response guard and the ARIA contract are all exercised live.

## Related

- Article EN: https://qapractices.com/test-cases/search-autocomplete-suggestion-test-cases/
- Article ES: https://qapractices.com/es/test-cases/search-autocomplete-suggestion-test-cases/
