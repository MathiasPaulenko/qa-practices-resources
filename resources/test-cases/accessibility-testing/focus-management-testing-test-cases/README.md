# Focus Management Test Cases — Companion Lab

Companion to the [Focus Management Test Cases](https://qapractices.com/test-cases/focus-management-testing-test-cases/) resource on QAPractices.com.

`focus_model.py` is a small stdlib-only Python model of the keyboard-focus contract: DOM tab order, positive `tabindex` hijacking, skip links, modal trap and return-to-trigger, removed-node fallbacks and `tabindex="-1"` script focus. It encodes the *rules* so the assertions can be exercised without a browser — the real-world checks use Playwright `keyboard` + `document.activeElement`, as shown in the resource.

## What the model covers

- **Tab order (TC-001/TC-010):** forward and `Shift+Tab` reverse follow DOM order; hidden nodes are skipped.
- **Skip links (TC-004):** first `Tab` reaches the link, activation lands on the main landmark.
- **Modal trap and return (TC-005):** focus mounts inside, cycles both directions, `Escape` restores the trigger — never `body`.
- **Positive tabindex (TC-007):** `tabindex > 0` is detected and shown to hijack the whole page order.
- **Dynamic removal (TC-012):** a removed focused node lands on a defined fallback, not `document.body`.
- **`tabindex="-1"` (TC-014):** absent from tab order, focusable by script.

## Run

```bash
pip install -r requirements.txt
pytest -v
```

Expected: `23 passed` in under a second — stdlib-only, no browser needed.

## Files

- `focus_model.py` — `Page`, `Focusable`, `Modal`, `FocusModelError`.
- `tests/test_focus_model.py` — 23 tests grouped by the resource's TC-ids.
- `requirements.txt`, `pytest.ini` — pytest 8.3.4 pinned.
