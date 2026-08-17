# Behave Priority Payment BDD Example

This folder contains a runnable **behave-priority** project that mirrors the payment example from the QAPractices guide [Behave Priority and Fail-Fast Guide](https://qapractices.com/documentation/behave-priority-guide/).

It shows how `@priority(N)`, `@critical` and `setup_priority()` sort scenarios and stop the suite early on a failure.

## Project structure

```text
payment-bdd/
├── pyproject.toml
├── requirements.txt
├── behave.ini
└── features/
    ├── environment.py
    ├── auth.feature
    ├── payment.feature
    ├── reporting.feature
    └── steps/
        └── payment_steps.py
```

## What it demonstrates

- `features/auth.feature` has two login scenarios with `@priority(1)` and `@priority(2)`.
- `features/payment.feature` has payment and refund scenarios at `@priority(3)` and `@priority(5)`.
- `features/reporting.feature` has a single scenario with no priority tag, so it defaults to `999`.
- `features/environment.py` wires `setup_priority(..., order=True, stop_after_failures=1, stop_on_critical=True, report=True)`.
- One scenario intentionally raises `AssertionError` to show fail-fast stopping the run.

## Run locally

```bash
cd payment-bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave
```

The suite runs in priority order and stops after the first failed critical scenario.
