# Third-Party API Integration Testing

> Printable companion and runnable examples for [Third-Party API Integration Test Cases](https://qapractices.com/test-cases/third-party-api-integration-testing).

This repository contains a printable version of the test case set plus example scripts you can adapt for your own project.

## Files

- `third-party-api-integration-testing.md` — Markdown version, ready to paste into a test management tool.
- `third-party-api-integration-testing.json` — Structured JSON with all test cases, edge cases and priorities.
- `scripts/` — Example scripts:
  - `test_auth.py` — pytest + requests for valid and invalid credentials.
  - `test_rate_limit.py` — pytest + requests for rate limit headers.
  - `test_webhook_signature.py` — Flask test client for webhook signature validation.
  - `wiremock_stubs.json` — WireMock stubs for 503 and timeout scenarios.

## How to use

1. Open `third-party-api-integration-testing.md` in your test management tool.
2. Copy `wiremock_stubs.json` into a WireMock instance for provider failure simulation.
3. Run `pytest scripts/test_auth.py` to test credential validation.
4. Run `pytest scripts/test_webhook_signature.py` to verify webhook integrity.

## Requirements

- Python 3.11+
- pytest 8.3+
- requests 2.32+
- Flask 3.0+
- WireMock (standalone or testcontainer)
