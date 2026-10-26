# Two-Factor Authentication Test Cases — Companion

Runnable materials for the [Two-Factor Authentication (2FA) Test Cases](https://qapractices.com/test-cases/two-factor-authentication-test-cases/) resource on QAPractices.

## Contents

| File | What it is |
|---|---|
| `totp_service.py` | Dependency-free TOTP service: RFC 6238 code generation and verification (HMAC-SHA-1, 30s steps, 6 digits), single-use enforcement, a 5-attempt lockout, configurable clock drift, and single-use backup codes. |
| `webauthn_service.py` | WebAuthn ceremony simulator: challenge issuance with a 60s TTL, single-use challenges, origin binding, credential registration and revocation — the server-side state machine behind TC-014, without real attestation crypto. |
| `login_gateway.py` | Minimal 2FA login gateway: password login that only yields a pre-auth token while 2FA is pending, client-flag bypass attempts ignored, codes bound to the requesting account, and role-based `2fa_enrollment_required` enforcement (TC-015, TC-016). |
| `test_two_factor.py` | pytest suite mapped to the TC-### cases: valid code, wrong code, replay, expired window, drift tolerance, lockout blocking valid codes, backup-code consumption and exhaustion, secret entropy. |
| `test_webauthn.py` | pytest suite for TC-014 and the ceremony-timeout edge case: enrollment challenge, successful assertion, wrong-origin rejection, revocation, expired and replayed challenges. |
| `test_login_gateway.py` | pytest suite for TC-015/016: pre-auth state instead of a session, injected `2fa_verified`/`skip_2fa` flags ignored, pre-auth token rejected on authenticated routes, cross-account code rejection, and admin enrollment enforcement. |
| `requirements.txt` | Only `pytest` — the services are pure stdlib (`hmac`, `hashlib`, `base64`, `secrets`, `struct`, `time`). |

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
- `WebAuthnService` checks challenge freshness, kind and origin before consuming the challenge — the same order a real RP uses when validating `clientDataJSON`. Pass `origin=` to exercise the origin-binding rejection from TC-014 step 4.
- `LoginGateway.login()` accepts arbitrary keyword flags on purpose: passing `2fa_verified=True` or `skip_2fa=True` must still return the pre-auth state, which is exactly what TC-015 asserts.
