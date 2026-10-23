# Two-Factor Authentication Test Cases — Companion

Runnable materials for the [Two-Factor Authentication (2FA) Test Cases](https://qapractices.com/test-cases/two-factor-authentication-test-cases/) resource on QAPractices.

## Contents

| File | What it is |
|---|---|
| `totp_service.py` | Dependency-free TOTP service: RFC 6238 code generation and verification (HMAC-SHA-1, 30s steps, 6 digits), single-use enforcement, a 5-attempt lockout, configurable clock drift, and single-use backup codes. |
| `test_two_factor.py` | pytest suite mapped to the TC-### cases: valid code, wrong code, replay, expired window, drift tolerance, lockout blocking valid codes, backup-code consumption and exhaustion, secret entropy. |
| `requirements.txt` | Only `pytest` — the service itself is pure stdlib (`hmac`, `hashlib`, `base64`, `secrets`, `struct`, `time`). |

## Quick start

```bash
pip install -r requirements.txt
pytest -v
```

Try the service directly:

```bash
python -c "
from totp_service import TOTPService
svc = TOTPService()
secret = svc.generate_secret('alice@example.com', issuer='UrbanThreads')
code = svc.current_code(secret)
print(secret, code, svc.verify(secret, code))
"
```

## Notes

- `verify(secret, code, at=...)` accepts a fake timestamp, so the tests can exercise window expiry and ±1-step drift without sleeping.
- `MAX_ATTEMPTS` locks the account at 5 failures — and a valid code is still rejected while locked, matching TC-007's expected result.
- Backup codes are stored in a set and removed on use; `remaining_backup_codes()` exposes exhaustion for TC-006.
- The drift parameter is deliberately off by default (`drift=0`): accepting an adjacent window is a documented policy decision, not a silent default.
