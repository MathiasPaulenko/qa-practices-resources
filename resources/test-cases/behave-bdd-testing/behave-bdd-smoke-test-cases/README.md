# Behave BDD Smoke Test Cases — Runnable Project

> Companion for [Behave BDD Smoke Test Cases](https://qapractices.com/test-cases/behave-bdd-smoke-test-cases) on QAPractices.

A minimal Behave project that implements the smoke wiring checks from the resource: `environment.py` hooks, `@smoke` tag filtering, data tables, scenario outlines, dry-run mode and exit codes.

## Requirements

- Python 3.11, 3.12 or 3.13
- `behave==1.3.3`, `behave-steplib==1.5.1` (pinned in `requirements.txt`)

## Run

```bash
python -m venv .venv && .venv/Scripts/activate   # Windows
pip install -r requirements.txt

behave --tags=smoke          # smoke gate — 4 scenarios
behave --dry-run             # parse + step-match only, no hooks
behave                       # full suite including @regression
behave --tags="smoke,~slow"  # negative tag expression example
```

Expected: `@smoke` scenarios pass, the `@regression` scenario is skipped by `--tags=smoke`, and a failing scenario makes the process exit with code 1.

## Files

- `behave.ini` — formatter and output capture settings.
- `features/environment.py` — `before_all` hook that sets `context.global_flag` (TC-004).
- `features/smoke.feature` — `@smoke` scenarios, a data table, a scenario outline and a `@regression` scenario for tag filtering (TC-003, TC-006, TC-007, TC-012).
- `features/steps/smoke_steps.py` — step definitions for the smoke scenarios (TC-005).
