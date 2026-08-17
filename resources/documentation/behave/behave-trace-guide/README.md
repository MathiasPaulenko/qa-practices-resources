# Behave Trace Inventory Example

This folder contains a runnable **behave-trace** project that mirrors the inventory example from the QAPractices guide [Behave Trace Guide](https://qapractices.com/documentation/behave-trace-guide/).

It is a minimal Behave BDD suite that shows how `behave-trace 1.3.1` captures step results, logs, text attachments and a failing scenario.

## Project structure

```text
inventory-trace/
├── pyproject.toml
├── behave.ini
├── requirements-dev.txt
├── inventory_service.py
└── features/
    ├── environment.py
    ├── inventory.feature
    ├── insufficient_stock.feature
    └── steps/
        └── inventory_steps.py
```

## What it demonstrates

- `features/inventory.feature` has two passing scenarios (shipment and order).
- `features/insufficient_stock.feature` has one scenario that intentionally fails with a `ValueError`, so you can inspect the trace.
- `features/environment.py` attaches a `step.txt` note and logs after every step.
- `behave.ini` selects the `behave-trace` formatter and writes `trace.json`.
- `pyproject.toml` pins `behave==1.3.3` and `behave-trace==1.3.1`.
- `.github/workflows/behave-trace.yml` generates the trace in CI and uploads it when a scenario fails.

## Run locally

```bash
cd inventory-trace
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
behave
```

Open the trace in the viewer:

```bash
behave-trace show trace.json
```

Run with `behave-trace run` for live reload:

```bash
behave-trace run . --watch
```

## CI

The GitHub Actions workflow runs `behave --format behave-trace -o trace.json` and uploads `trace.json` as an artifact only when the suite fails.

## Note

The `insufficient_stock.feature` is intentionally failing. It is there to show how `behave-trace` records the error, the skipped `Then` step and the attached logs.
