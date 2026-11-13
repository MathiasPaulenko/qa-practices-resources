# Ad Monetization in Games Test Cases — Runnable Companion

Offline fakes that make the two most failure-prone mechanics in ad monetization testable without a device, a network or an ad SDK:

- `FakeRewardedAdSDK` — only fires `on_user_earned_reward` after a complete view; early closes and replays grant nothing.
- `RewardLedger` — drains `pending_reward` exactly once, so double-grant bugs surface as assertion failures.
- `FrequencyCapper` — interval-based impression cap driven by the system clock, so freezegun can test window boundaries deterministically.

Companion to [Ad Monetization in Games Test Cases](https://qapractices.com/test-cases/ad-monetization-games-testing/) ([versión en español](https://qapractices.com/es/test-cases/ad-monetization-games-testing/)).

## Setup

```bash
pip install -r requirements.txt
pytest tests/ -q
```

## Mapping to the article

| Test | Test case |
|---|---|
| `test_rewarded_ads.py` | TC-01 — reward granted once, only on the completion callback |
| `test_frequency_cap.py` | TC-08 — cap enforced inside the window, reset after it |
| `features/rewarded_ads.feature` | TC-01 — same scenarios in Gherkin for BDD handoff |
