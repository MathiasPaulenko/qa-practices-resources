# Behave Retry Payment BDD Example

This folder contains a runnable **behave-retry** project that mirrors the payment example from the QAPractices guide [Behave Retry Guide](https://qapractices.com/documentation/behave-retry-guide/).

It shows how `@flaky` and `@retry:N` tags make Behave re-execute failing scenarios that match specific exceptions.

## Project structure

```text
payment-bdd/
├── pyproject.toml
├── requirements.txt
├── behave.ini
└── features/
    ├── environment.py
    ├── payment.feature
    └── steps/
        └── payment_steps.py
```

## What it demonstrates

- `features/payment.feature` has three scenarios.
- The `@flaky` charge scenario fails once with `TimeoutError` and then passes on retry.
- The `@flaky @retry:3` refund scenario overrides `max_retries` and passes on the third attempt.
- The normal charge scenario is not retried.
- `features/environment.py` wires `setup_retry()` with `max_retries=2`, tag filtering and exponential backoff.

## Run locally

```bash
cd payment-bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave
```

The retry report at the end shows how many scenarios were retried and how many passed on retry.
