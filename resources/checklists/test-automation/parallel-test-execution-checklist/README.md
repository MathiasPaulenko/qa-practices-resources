# Parallel Test Execution Checklist — Companion

Runnable artifacts for the [Parallel Test Execution Checklist](https://qapractices.com/checklists/parallel-test-execution-checklist/) on QAPractices.com.

## Files

| File | Purpose |
|------|---------|
| `pytest_parallel.ini` | pytest-xdist config: 4 workers, `loadgroup` distribution, per-worker JUnit reports, seeded order. |
| `github_actions_sharding.yml` | GitHub Actions workflow: deterministic 4-way Playwright sharding plus a merge job producing one HTML report. |
| `worker_isolation.py` | pytest helpers that give each xdist worker its own database schema, port range, and test-user namespace. |

## Quick start

```bash
# 1. pytest-xdist on one machine
pip install pytest-xdist
pytest -c pytest_parallel.ini tests/

# 2. Sharding across CI machines
#    copy github_actions_sharding.yml to .github/workflows/e2e-sharded.yml

# 3. Worker-scoped resources in your conftest.py
from worker_isolation import worker_schema, worker_db_url
```

## The rule that matters

Isolate before you scale. Workers sharing a database, a port range, or a test user pool will race — and the failures look exactly like flaky tests.
