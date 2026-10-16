# Webhook Retry and Dead Letter Queue Testing Checklist — Companion

Companion resource for [Webhook Retry and Dead Letter Queue Testing Checklist](https://qapractices.com/checklists/webhook-retry-dead-letter-queue-testing-checklist).

## Contents

- `webhook_client.py` — reference webhook sender with exponential backoff, jitter, `Retry-After` support and an in-memory dead letter queue
- `tests/test_webhook_retry.py` — pytest suite covering backoff delays, permanent 4xx routing, `Retry-After` honoring, timeout retries, DLQ replay and duplicate rejection
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.12+ with requests 2.32, responses 0.25 and pytest 8.3

## Usage

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

All tests run against mocked HTTP endpoints (`responses`), so no real receiver is needed. To point the client at a real endpoint, pass its URL as the first argument of `deliver_webhook()`.
