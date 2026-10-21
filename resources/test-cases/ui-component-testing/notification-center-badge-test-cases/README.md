# Notification Center Badge Test Cases — Companion

Companion resource for [Notification Center Badge Test Cases: Count, Unread, Clear](https://qapractices.com/test-cases/notification-center-badge-test-cases/).

## Contents

- `badge_engine.py` — stdlib-only model of the badge counter: `NotificationServer` as source of truth (push with id-dedup, mark-read, mark-all-read, delete, TTL expiry, audit log) and `BadgeTab` as one tab's view (hydration, offline honesty, reconnect resync) connected through a `BroadcastChannel` stand-in.
- `badge.html` — static fixture implementing the real component for manual and Playwright verification: bell icon with badge element, `notif:push` event + `window.pushNotification` API, BroadcastChannel cross-tab sync, mark-all-read, `aria-label` count and `prefers-reduced-motion` support. Open it in any browser.
- `tests/conftest.py` — puts the engine on `sys.path`.
- `tests/test_badge_engine.py` — executable subset of the article's cases: unread count (TC-001), WS increment (TC-002), idempotent decrement (TC-003), mark-all-read (TC-004), 99+ cap (TC-005), zero hides (TC-006/TC-017), session persistence (TC-007), offline honesty (TC-012), cross-tab convergence (TC-013), push dedup (boundary), clear-vs-inflight race (boundary), shared delete (TC-018), TTL expiry (TC-029), flood dedup (TC-016), audit trail (TC-030) and account switch (TC-028).

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Expected output: `16 passed`.

## Related

- Article EN: https://qapractices.com/test-cases/notification-center-badge-test-cases/
- Article ES: https://qapractices.com/es/test-cases/notification-center-badge-test-cases/
