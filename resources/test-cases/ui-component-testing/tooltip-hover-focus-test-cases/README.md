# Tooltip Hover Focus Test Cases — Companion

Companion resource for [Tooltip Hover Focus Test Cases: Delay, Position, Content](https://qapractices.com/test-cases/tooltip-hover-focus-test-cases/).

## Contents

- `tooltip_engine.py` — stdlib-only model of the tooltip lifecycle used in the article: virtual-clock `TooltipController` (show/hide delays, transit suppression, Escape suppression, instant exits for scroll/unmount, focus/blur parity), `resolve_position` (auto-flip with preferred side + fallback order + viewport clamp) and `check_aria_contract` (role/aria-describedby wiring).
- `tooltip.html` — static fixture implementing the real component for manual and Playwright verification: help icon, icon-only toolbar buttons, disabled Publish with focusable wrapper, truncated sidebar label, top/right edge triggers with auto-flip, Escape dismiss and `prefers-reduced-motion` support. Open it in any browser.
- `tests/conftest.py` — puts the engine on `sys.path`.
- `tests/test_tooltip_engine.py` — executable subset of the article's cases: delay gating (TC-002), transit never mounts (boundary row 1), gap crossing cancels hide (TC-013/TC-022), Escape suppression (TC-007), focus/blur parity (TC-006), instant exits (TC-018/boundary row 4), empty content (TC-016), persistence (TC-026), top→bottom and right→left flips (TC-011/TC-012), clamped fallback (TC-024) and the ARIA contract (TC-021/boundary row 5).

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
cd resources/test-cases/ui-component-testing/tooltip-hover-focus-test-cases
pytest tests/ -v
```

Manual checks: open `tooltip.html` in a browser — hover the "ⓘ" icon, Tab to it, press Escape, and scroll to see the instant exits.

## What this covers

- `TooltipController` — the timing contract (500ms show, 300ms hide) and the event model behind the boundary table.
- `resolve_position` — the auto-flip decision tree behind TC-011, TC-012 and TC-024.
- `check_aria_contract` — the `role="tooltip"` / `aria-describedby` wiring behind TC-021.
- `tooltip.html` — manual fixture for the Playwright snippet in the article's Automation Example section.
