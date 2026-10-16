# Release Testing Test Cases: Runnable Smoke-Gate Suite

Companion to the QAPractices guide [Release Testing Test Cases: Smoke, Regression & Deploy](https://qapractices.com/test-cases/release-testing-test-cases/).

A Flask mini-app that simulates a deployed service — `/health` with dependency probes, environment metadata, artifact checksums, feature flags and a rollback endpoint — plus a pytest 8.3 suite implementing the automatable parts of the guide: RT-SM-03/04, RT-ENV-01/04 and the release-specific edge cases.

## Project structure

```text
├── app.py                          # Flask app: health, env metadata, flags, rollback
├── tests/test_release_smoke.py     # pytest suite: smoke + environment + edge cases
├── .github/workflows/release-gate.yml  # post-deploy gate example (deployment_status)
└── requirements.txt
```

## Concept mapping

| Test case | What it proves | Function |
|---|---|---|
| RT-SM-03 | `/health` returns 200 in under 500 ms | `test_health_endpoint_200_and_fast` |
| RT-SM-03/04 | Every dependency reports `up`; degraded when one fails | `test_health_*`, `test_health_degrades_when_a_dependency_is_down` |
| RT-ENV-01 | The suite refuses a non-production target | `test_environment_*` |
| RT-ENV-04 | No pending migrations in the release | `test_no_pending_migrations`, `test_pending_migrations_are_detected` |
| Edge: checksum | Deployed artifact hash must match the build hash | `test_artifact_checksum_*`, `test_checksum_mismatch_is_detected` |
| Edge: rollback window | Rollback allowed inside the window, rejected (409) past it | `test_rollback_*` |

## Requirements

- Python 3.10+, `pip install -r requirements.txt` (Flask 3.x, pytest 8.3).

## Usage

```bash
pip install -r requirements.txt
pytest -v
```

No server needed — the tests use Flask's test client. To poke the app by hand:

```bash
python app.py            # serves on :5000
curl http://localhost:5000/health
curl http://localhost:5000/meta/environment
```

Simulate failure modes with environment variables — e.g. `CACHE_UP=0`, `PENDING_MIGRATIONS=2`, `APP_ENV=staging`, `ARTIFACT_SHA=deadbee`, or a `DEPLOY_STARTED_AT` timestamp older than the 30-minute rollback window.

For real deployments the same tests run against a live URL instead of the test client — the guide shows the `requests` variant and the GitHub Actions `deployment_status` gate (`release-gate.yml`).

## Notes

- The article and this suite stay versioned together: pytest 8.3, requests 2.32, Flask 3.x.
- Spanish version: `README.es.md`.
