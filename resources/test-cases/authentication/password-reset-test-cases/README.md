# Password Reset Test Cases — Runnable Companion

Companion resource for [Password Reset Test Cases: Token, Email & Security](https://qapractices.com/test-cases/password-reset-test-cases/) on QAPractices.com.

## What's inside

- `tests/` — pytest 8.3 scripts covering the 16 test cases from the resource.
- `postman/` — Postman collection with the reset-request and reset-confirm endpoints, ready to run against a staging API.

## Requirements

- Python 3.10+
- pytest 8.3+
- requests 2.32+
- A staging API exposing `/auth/reset-request` and `/auth/reset-confirm`
- MailHog v1.0 (or similar) for email capture in staging

Install dependencies:

```bash
pip install -r tests/requirements.txt
```

## Running the tests

```bash
pytest tests/ -v --json-report --json-report-file=reports/report.json
```

The tests use the `BASE_URL` environment variable (default: `https://demo-api.qapractices.test`). Point it at your staging API before running:

```bash
export BASE_URL=https://your-staging-api.example.com
pytest tests/ -v
```

## Postman collection

Import `postman/password-reset-test-cases.postman_collection.json` into Postman v11+. The collection includes:

- Reset request (valid email)
- Reset request (unregistered email)
- Reset confirm (valid token)
- Reset confirm (expired token)
- Reset confirm (reused token)
- Rate limit burst (6 rapid requests)

## Test coverage

| Script | Test cases covered |
| --- | --- |
| `test_reset_request.py` | TC-001, TC-006, TC-007 |
| `test_reset_confirm.py` | TC-002, TC-004, TC-005, TC-013 |
| `test_token_security.py` | TC-008, TC-009, TC-012, TC-014, TC-015 |
| `test_password_policy.py` | TC-003, TC-010 |
| `test_rate_limiting.py` | TC-011 |
| `test_audit_log.py` | TC-016 |

## Related resource

- [Password Reset Test Cases: Token, Email & Security](https://qapractices.com/test-cases/password-reset-test-cases/)
- [Authentication Testing Checklist](https://qapractices.com/checklists/authentication-checklist)
- [Authentication topic](https://qapractices.com/topics/authentication)
