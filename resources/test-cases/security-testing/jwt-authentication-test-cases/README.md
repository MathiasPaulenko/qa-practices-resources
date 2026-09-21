# JWT Authentication Test Cases — Companion Lab

Runnable lab for the [JWT Authentication Test Cases](https://qapractices.com/test-cases/jwt-authentication-test-cases/) resource on QAPractices.

A minimal Flask app issues RS256 access + refresh token pairs and exposes the same profile endpoint twice: `/secure/api/profile` verifies correctly (pinned algorithm, full claim check, `jti` denylist) while `/vulnerable/api/profile` trusts the token's own `alg` header — the bug behind `alg=none` and RS256→HS256 confusion — and never consults the denylist. The pytest suite fires the attacks from the resource at both and asserts the observable difference.

## Requirements

- Python 3.10+
- `pip install -r requirements.txt`

## Run

```bash
pytest -v
```

Expected: all 10 tests pass. Each test documents the vulnerable behavior *and* the protected behavior — the suite is green because both sides behave as designed.

## What each test verifies

| Test | Maps to | Demonstrates |
|---|---|---|
| `test_valid_token_grants_access_on_secure` | TC-JWT-001 | Correctly signed, unexpired token → HTTP 200 |
| `test_expired_token_rejected_on_both` | TC-JWT-002 | `exp` in the past → HTTP 401 on both verifiers |
| `test_tampered_payload_rejected_on_both` | TC-JWT-003 | `role` flipped to `admin` without resigning → HTTP 401 |
| `test_alg_none_accepted_on_vulnerable` | TC-JWT-004 | Unsigned `alg=none` token → HTTP 200 as `admin` |
| `test_alg_none_rejected_on_secure` | TC-JWT-004 | Same token → HTTP 401 |
| `test_rs256_as_hs256_accepted_on_vulnerable` | TC-JWT-005 | Token signed with the public key as HMAC secret → HTTP 200 |
| `test_rs256_as_hs256_rejected_on_secure` | TC-JWT-005 | Same forged token → HTTP 401 |
| `test_refresh_rotation_and_replay_rejected` | TC-JWT-007 | First exchange rotates; replaying the consumed token revokes the whole family |
| `test_revoked_token_rejected_on_secure` | Edge table | Logout lands the `jti` on the denylist → replay returns 401 |
| `test_revoked_token_still_valid_on_vulnerable` | Edge table | No denylist → the same token keeps working until `exp` |

## Notes

- Keys are generated at import — no setup, no state between runs.
- `pytest.ini` sets `pythonpath = .` so tests import `app.py` directly.
- PyJWT 2.x refuses to use an asymmetric key as an HMAC secret, so the confusion forge signs the token by hand with `hmac` — exactly how the real attack works.
- The vulnerable code exists for training only. Never let the token's `alg` header pick your verification key.
