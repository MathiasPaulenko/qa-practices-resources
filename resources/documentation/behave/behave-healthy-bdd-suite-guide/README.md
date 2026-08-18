# Shop BDD — Healthy Behave Suite Demo

This is a minimal Behave BDD project that demonstrates a healthy suite structure and includes a `health_check.py` script to audit it.

## What it contains

- `shop.py` — small catalog and cart domain.
- `features/cart.feature` — cart scenarios.
- `features/inventory.feature` — inventory scenario.
- `features/steps/catalog_steps.py` — shared catalog step with a `Price` type.
- `features/steps/cart_steps.py` — cart step definitions.
- `features/steps/inventory_steps.py` — inventory step definitions.
- `features/environment.py` — per-scenario context setup.
- `scripts/health_check.py` — detects duplicate step patterns and risky tags.
- `behave.ini` and `pyproject.toml` — minimal project configuration.

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## Run the suite

```bash
behave --dry-run
behave
```

## Run the health check

```bash
python scripts/health_check.py
```

## Full guide

See the [QAPractices guide](https://qapractices.com/documentation/behave-healthy-bdd-suite-guide) for metrics, CI setup, debugging and scaling patterns.
