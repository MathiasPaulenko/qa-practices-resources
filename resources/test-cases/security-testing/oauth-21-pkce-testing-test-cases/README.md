# OAuth 2.1 & PKCE Test Cases — Companion

> pytest framework for the [OAuth 2.1 & PKCE Test Cases](https://qapractices.com/test-cases/oauth-21-pkce-testing-test-cases/) resource on QAPractices.com

## What's included

- `pkce_utils.py` — PKCE pair generation (S256 and plain for negative tests)
- `mock_auth_server.py` — In-memory mock OAuth 2.1 authorization server with S256 enforcement, code lifecycle, refresh rotation and scope validation
- `conftest.py` — Pytest fixtures for all test cases
- `test_oauth_pkce.py` — TC-01 through TC-10 as parametrized pytest tests

## Quick start

```bash
pip install pytest 8.3
pytest test_oauth_pkce.py -v
```

## Test cases

| Test | Description |
| ---- | ----------- |
| TC-01 | Valid authorization code flow with S256 PKCE |
| TC-02 | Missing `code_challenge` rejected |
| TC-03 | `plain` method rejected, `S256` accepted |
| TC-04 | Verifier mismatch rejected |
| TC-05 | Expired authorization code rejected |
| TC-06 | Authorization code replay rejected |
| TC-07 | Redirect URI strict validation (trailing slash fails) |
| TC-08 | State parameter CSRF protection |
| TC-09 | Refresh token rotation invalidates old token |
| TC-10 | Scope enforcement (ungranted scope rejected) |

## Using against a real server

The `mock_auth_server.py` is a reference implementation. To test against a real authorization server, replace the mock with `requests` calls to your server's endpoints. The test structure remains the same.

## Requirements

- Python 3.10+
- pytest 8.3+

## License

MIT — see [QAPractices.com](https://qapractices.com) for terms.
