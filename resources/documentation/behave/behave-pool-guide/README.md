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

Expected output with behave-pool 1.3.0:

```text
USING RUNNER: behave_pool.runner:ParallelRunner
feature:features/checkout.feature ... passed (0.02s)
feature:features/inventory.feature ... passed (0.02s)
feature:features/payment.feature#serial ... passed (0.00s)
3 features, 4 scenarios, 13 steps - passed: 13, failed: 0, skipped: 0, undefined: 0
```

After the run, the project root contains:

- `.behave-pool-timing.json` — historical durations used by LPT scheduling.
- `behave-pool-report.json` — unified `behave-modern-json-report` artifact.

## Run sequentially for debugging

```bash
behave --jobs 1
```

## Sharding in CI

The GitHub Actions workflow runs `behave-pool --shard INDEX/TOTAL --parallel-report ...` per matrix job and uploads each shard's `behave-pool-report.json` as a separate artifact. The same pattern can be adapted to GitLab CI with `CI_NODE_INDEX` and `CI_NODE_TOTAL`.
