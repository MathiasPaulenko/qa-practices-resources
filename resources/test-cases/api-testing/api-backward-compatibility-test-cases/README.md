# API Backward Compatibility — Runnable Companion

Runnable companion for the [API Backward Compatibility Test Cases: TaskFlow Example](https://qapractices.com/test-cases/api-backward-compatibility-test-cases/) guide on QAPractices.

A stdlib mock server implements the TaskFlow versioning contract described in the guide — `API-Version` header negotiation, the `2025-01`/`2026-07` schema split (`assignee_id` → `assignee`), `Deprecation`/`Sunset` headers (RFC 9745 / RFC 8594) and a retired `2024-03` version that answers `410 Gone`. A pytest 8.3 suite exercises the same cases as the guide's test-case tables.

## Contents

- `mock_server.py` — the TaskFlow fixture: header-based versioning, dual-shipped deprecated field, enum validation, rate-limit headers, sunset enforcement
- `tests/test_version_negotiation.py` — TC-001 to TC-004: old/new contract, missing header default, unsupported version
- `tests/test_field_compatibility.py` — TC-005 to TC-007 + edge rows: dual-shipped field, optional field boundary, enum removal, old-client write mapping
- `tests/test_deprecation_sunset.py` — TC-016: `410 Gone` with `Link: rel="successor-version"`, `Sunset` header on the stable version
- `tests/test_contract_stability.py` — TC-008/010/013/014/015: pagination, error shape, HTTP methods, auth and rate-limit headers across versions
- `requirements.txt` — pytest 8.3 + requests

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
pytest tests/ -v
```

The mock server also runs standalone for manual checks:

```bash
python mock_server.py 8571
curl -H "Authorization: Bearer test" -H "API-Version: 2025-01" http://127.0.0.1:8571/v1/tasks/T-301
curl -H "Authorization: Bearer test" -H "API-Version: 2024-03" -i http://127.0.0.1:8571/v1/tasks/T-301   # 410 Gone
```

The point of the fixture: version-compatibility bugs only surface when an old client meets a new contract — the mock encodes the transition behaviors (dual-shipped `assignee_id`, mapped old-client writes, sunset enforcement) so every case in the guide is reproducible locally without a real TaskFlow deployment.
