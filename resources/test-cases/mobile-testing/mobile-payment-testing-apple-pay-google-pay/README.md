# Mobile Payment Test Cases — Companion

Runnable artifacts for [Mobile Payment Test Cases: Apple Pay & Google Pay](https://qapractices.com/test-cases/mobile-payment-testing-apple-pay-google-pay/) on QAPractices.

## Contents

| File | Purpose | Related TC |
|---|---|---|
| `python/apple_receipt_validation.py` | Verify Apple receipts against `verifyReceipt` (handles the 21007 sandbox redirect) | TC-MP-006, TC-MP-007, TC-MP-008 |
| `python/pan_in_logs_test.py` | pytest check that no PAN/card data leaks into app logs | TC-MP-011 |
| `scripts/sandbox-setup-checklist.md` | Environment checklist for Apple Pay / Google Pay / IAP sandbox testing | all |

## Requirements

- Python 3.12+, `requests` 2.32+, `pytest` 8.3+.
- `APPLE_SHARED_SECRET` and `RECEIPT_DATA` env vars for receipt validation.
- An `app.log` file in the working directory for the PAN check.

## Usage

```bash
# Validate a receipt (sandbox)
RECEIPT_DATA=... APPLE_SHARED_SECRET=... python python/apple_receipt_validation.py

# Scan logs for card data
pytest python/pan_in_logs_test.py -v
```

Spanish version: [README.es.md](README.es.md)
