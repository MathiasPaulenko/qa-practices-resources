# AI API Rate Limit & Throttling Test Cases — Companion

Companion resource for [AI API Rate Limit & Throttling Test Cases: 16 Scenarios](https://qapractices.com/test-cases/ai-api-rate-limit-throttling-test-cases/).

## Contents

- `fake_provider.py` — stdlib `http.server` implementing per-key + per-model RPM buckets, TPM and daily token quotas, `Retry-After` (seconds or HTTP-date), OpenAI-style `x-ratelimit-*` headers, and a 529 overload mode via `X-Force-Status`. The window is configurable down to milliseconds so quota resets are testable without real waiting.
- `client.py` — client harness: `parse_retry_after` (delta-seconds + HTTP-date), `call_with_backoff` (honors `Retry-After`, exponential backoff with jitter, retry cap), and an SSE truncation check (`[DONE]` sentinel).
- `tests/test_rate_limits.py` — 17 tests mapped to the TC IDs: within-limit, exact boundary, burst, TPM exhaustion, `Retry-After`, jitter spread, retry cap, per-key and per-model scopes, mid-stream truncation, fallback degradation, 529 handling, headers, quota reset, plus daily-quota and HTTP-date edges.

## Requirements

- Python 3.10+, `pip install -r requirements.txt`

## Usage

```bash
pytest tests/ -q
```

Expected output: `17 passed`.

No real provider quota is consumed — every case runs against the local fake provider or a stubbed session.

## Related

- Article EN: https://qapractices.com/test-cases/ai-api-rate-limit-throttling-test-cases/
- Article ES: https://qapractices.com/es/test-cases/ai-api-rate-limit-throttling-test-cases/
