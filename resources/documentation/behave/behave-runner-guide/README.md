# Behave Runner Payment BDD Example

This folder contains a runnable **behave-runner** project that mirrors the payment example from the QAPractices guide [Behave Runner CLI Guide](https://qapractices.com/documentation/behave-runner-guide/).

It is a tiny payment BDD suite with smoke, regression and critical scenarios, plus `pyproject.toml` profiles and a GitHub Actions workflow.

## Project structure

```text
payment-bdd/
├── .github/
│   └── workflows/
│       └── behave.yml
├── pyproject.toml
├── behave.ini
├── requirements-dev.txt
├── features/
│   ├── environment.py
│   ├── payment.feature
│   └── steps/
│       └── payment_steps.py
```

## What it demonstrates

- `features/payment.feature` has three scenarios tagged with `@smoke`, `@critical` and `@regression`.
- `features/steps/payment_steps.py` implements the steps with simple in-memory state.
- `pyproject.toml` defines a `smoke` profile (tag filter) and a `ci` profile (parallel, JSON report, `reports/report.json` output).
- `behave.ini` shows the same settings using the flat dot-notation that `behave-runner` supports.
- `.github/workflows/behave.yml` installs the runner, runs the `ci` profile and uploads the JSON report.

## Run locally

```bash
cd payment-bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
behave-runner run
```

Run a profile:

```bash
behave-runner run --profile smoke
```

List scenarios without running them:

```bash
behave-runner list --format json
```

Select only smoke scenarios:

```bash
behave-runner select --tags '@smoke' --format names
```

Watch files during development:

```bash
behave-runner watch
```

Generate an HTML report:

```bash
behave-runner report generate --format html
```

## CI

The GitHub Actions workflow runs `behave-runner run --profile ci` and uploads `reports/report.json` as an artifact.
