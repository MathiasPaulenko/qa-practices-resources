# Biometric Auth Lab

Runnable companion for [Mobile Biometric Authentication Testing: Face ID, Touch ID](https://qapractices.com/test-cases/mobile-biometric-authentication-testing/) — a stdlib-only Python model of the biometric auth state machine: match attempts, OS lockout after five failures, device credential fallback, enrollment-change key invalidation and session expiry.

## Run

```bash
pip install -r requirements.txt
pytest -v
```

## What it covers

| Test | Suite case |
|---|---|
| `test_successful_biometric_auth` | TC-001 happy path |
| `test_biometric_not_enrolled` | TC-002 hidden option |
| `test_lockout_after_five_failures` | TC-003 OS lockout |
| `test_correct_biometric_rejected_during_lockout` | TC-003 lockout holds |
| `test_second_lockout_becomes_permanent` | TC-003 permanent lockout |
| `test_enrollment_change_invalidates_credential` | TC-004 key invalidated |
| `test_reenroll_after_invalidated_credential` | TC-004 fresh credential |
| `test_backgrounding_during_prompt_returns_to_login` | TC-005 backgrounding |
| `test_no_device_security_hides_biometric` | TC-006 no passcode |
| `test_no_sensor_reports_no_hardware` | Edge: missing sensor |
| `test_session_expiry_requires_reauth` | TC-007 session timeout |
| `test_rooted_device_blocks_biometric` | TC-008 rooted device |
| `test_device_credential_fallback` | TC-009 passcode fallback |
| `test_wrong_passcode_does_not_clear_lockout` | TC-009 wrong credential |
| `test_user_cancel_no_retry_loop` | TC-010 cancel path |
| `test_prompt_timeout` | Edge: idle prompt |

## Notes

- `biometric_auth.py` mirrors the platform error surface: `LAError.biometryLockout` becomes `BiometricError.LOCKOUT`, `BIOMETRIC_ERROR_LOCKOUT_PERMANENT` becomes `LOCKOUT_PERMANENT`, and `Keychain biometryCurrentSet` / `setInvalidatedByBiometricEnrollment(true)` becomes the enrolled-set snapshot check.
- This is a logic-level lab, not a UI test. For on-device coverage use Appium 2.x `mobile:sendBiometricMatch` on emulators, or Espresso/XCUITest on real hardware — emulators cannot reproduce sensor noise or anti-spoofing.
- The lockout policy models iOS/Android behavior: five consecutive failures lock biometrics until a correct device passcode clears them; a second lockout cycle becomes permanent.
