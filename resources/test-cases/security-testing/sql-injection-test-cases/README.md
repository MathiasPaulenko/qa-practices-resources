# SQL Injection Test Cases — Companion Lab

Runnable lab for the [SQL Injection Test Cases](https://qapractices.com/test-cases/sql-injection-test-cases/) resource on QAPractices.

A minimal Flask + SQLite app exposes the same features twice: `/vulnerable/*` endpoints build SQL by string concatenation (intentionally injectable), and `/secure/*` endpoints use parameterized queries. The pytest suite fires the payloads from the resource at both and asserts the observable difference — this is what "expected result: vulnerable vs secure" looks like when it actually executes.

## Requirements

- Python 3.10+
- `pip install -r requirements.txt`

## Run

```bash
pytest -v
```

Expected: all tests pass. Each test documents the vulnerable behavior *and* the protected behavior — the suite is green because both sides behave as designed.

## What each test verifies

| Test | Maps to | Demonstrates |
|---|---|---|
| `test_normal_login_works_on_both_endpoints` | Baseline | Both login forms accept real credentials |
| `test_vulnerable_login_bypassed_by_classic_payload` | TC-SQLI-001 | `' OR '1'='1'--` logs in as `admin` without a password |
| `test_vulnerable_login_naive_payload_does_not_bypass` | TC-SQLI-001 | Bare `' OR '1'='1` fails — `AND` binds tighter than `OR`, so the password check still holds |
| `test_secure_login_treats_payload_as_literal` | TC-SQLI-001 | Payload → HTTP 401, treated as a literal string |
| `test_vulnerable_search_allows_union_exfiltration` | TC-SQLI-002 | UNION payload leaks usernames + password hashes into product results |
| `test_secure_search_treats_union_as_literal` | TC-SQLI-002 | Same payload → empty result set |
| `test_vulnerable_numeric_param_returns_all_rows` | Edge table | `id=1 OR 1=1` returns the entire products table |
| `test_secure_numeric_param_rejects_expression` | Edge table | Same input → no rows |

## Notes

- The database is in-memory and seeded on import — no setup, no state between runs.
- `pytest.ini` sets `pythonpath = .` so tests can import `app.py` directly.
- The vulnerable code exists for training only. Never ship concatenated queries — the `/secure/*` endpoints show the intended pattern.
