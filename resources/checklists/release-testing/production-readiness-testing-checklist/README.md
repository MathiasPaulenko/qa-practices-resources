# Production Readiness Testing Checklist — Companion

Executable companion for the [Production Readiness Testing Checklist](https://qapractices.com/checklists/production-readiness-testing-checklist).

## Contents

- `release_gate_workflow.yml` — GitHub Actions go/no-go gate: artifact identity, production smoke suite, monitoring/alert coverage, migration rollback compatibility, drill recency and capacity headroom. Every step blocks the release on failure.
- `rollback_drill.sh` — rollback rehearsal script: times each runbook step (artifact revert, schema contract, smoke verify, alerts quiet) and logs results; also runs as a CI recency gate (`--check-recency --max-days 90`).

## Usage

```bash
# Rehearse rollback in staging and measure real timing
./rollback_drill.sh --rehearse staging

# CI gate: block release if last drill is older than 90 days
./rollback_drill.sh --check-recency --max-days 90
```

The workflow assumes helper scripts (`check_alert_coverage.py`, `check_migration_compat.py`, `check_capacity.py`) — implement them against your observability and migration tooling, or replace the steps with your equivalents.
