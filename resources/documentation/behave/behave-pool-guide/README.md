# Behave Pool Checkout Example

This folder contains a runnable **behave-pool** project that mirrors the parallel execution example from the QAPractices guide [Parallel Behave BDD Execution with behave-pool](https://qapractices.com/documentation/behave-pool-guide/).

It is a tiny `checkout-service` with inventory, cart, and payment scenarios that demonstrates feature-level parallelism, the `@serial` tag, LPT load balancing, and cross-runner sharding in GitHub Actions.

## Project structure

```text
checkout-service/
├── .github/
│   └── workflows/
│       └── behave-pool.yml
├── behave.ini
├── pyproject.toml
├── requirements.txt
├── checkout_service.py
├── features/
│   ├── environment.py
│   ├── inventory.feature
│   ├── checkout.feature
│   ├── payment.feature
│   └── steps/
│       └── checkout_steps.py
```

## What it demonstrates

- `checkout_service.py` is a tiny in-memory inventory, cart, and payment gateway used by the BDD suite.
- `features/inventory.feature` and `features/checkout.feature` run in parallel because they are isolated per feature.
- `features/payment.feature` contains an `@serial` scenario that cannot overlap with other scenarios (rate-limited gateway mock).
- `behave.ini` selects the parallel runner, sets `jobs = 4`, and configures LPT balancing and the unified JSON report.
- `.github/workflows/behave-pool.yml` runs a local parallel job and a sharded matrix job.

## Run locally

```bash
cd checkout-service
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave
```

Expected output on Linux/macOS:

```text
Feature: Inventory reservation
  Scenario: Reserve in-stock item ... passed
  Scenario: Reserve another in-stock item ... passed

Feature: Checkout cart
  Scenario: Calculate cart total ... passed

Feature: Payment processing
  @serial
  Scenario: Charge a card through the rate-limited gateway ... passed

3 features passed, 0 failed, 0 skipped
4 scenarios passed, 0 failed, 0 skipped
```

After the run, the project root contains:

- `.behave-pool-timing.json` — historical durations used by LPT scheduling.
- `behave-pool-report.json` — unified `behave-modern-json-report` artifact.

## Run sequentially for debugging

```bash
behave --jobs 1
```

## Sharding in CI

The GitHub Actions workflow writes a per-shard `behave.ini`, runs `behave features/`, and uploads each shard's `behave-pool-report.json` as a separate artifact. The same pattern can be adapted to GitLab CI with `CI_NODE_INDEX` and `CI_NODE_TOTAL`.
