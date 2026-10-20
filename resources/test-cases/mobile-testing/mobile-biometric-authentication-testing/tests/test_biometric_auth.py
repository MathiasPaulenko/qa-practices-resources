"""Tests for the biometric auth lab, mapped to TC-001..TC-010 of the resource."""

from __future__ import annotations

import pytest

from biometric_auth import (
    AuthenticatorClass,
    BiometricAuthError,
    BiometricAuthService,
    BiometricError,
    Device,
    MAX_ATTEMPTS,
)


class FakeClock:
    def __init__(self) -> None:
        self.t = 1_000_000.0

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def device() -> Device:
    return Device()


@pytest.fixture
def service(device: Device, clock: FakeClock) -> BiometricAuthService:
    return BiometricAuthService(device, clock)


def test_successful_biometric_auth(service: BiometricAuthService) -> None:
    """TC-001: enrolled biometric issues a biometric session."""
    session = service.authenticate("finger-1")
    assert session.method == "biometric"
    assert service.is_session_valid(session.token)


def test_biometric_not_enrolled(device: Device, clock: FakeClock) -> None:
    """TC-002: no enrollment hides the biometric option."""
    device.remove_all_biometrics()
    service = BiometricAuthService(device, clock)
    assert service.can_authenticate() is AuthenticatorClass.WEAK
    assert not service.biometric_option_visible()
    with pytest.raises(BiometricAuthError) as exc:
        service.authenticate("finger-1")
    assert exc.value.error is BiometricError.NOT_ENROLLED


def test_lockout_after_five_failures(service: BiometricAuthService) -> None:
    """TC-003: fifth consecutive failure triggers OS lockout."""
    for _ in range(MAX_ATTEMPTS - 1):
        with pytest.raises(BiometricAuthError) as exc:
            service.authenticate("wrong-finger")
        assert exc.value.error is BiometricError.NO_MATCH
    with pytest.raises(BiometricAuthError) as exc:
        service.authenticate("wrong-finger")
    assert exc.value.error is BiometricError.LOCKOUT


def test_correct_biometric_rejected_during_lockout(
    service: BiometricAuthService,
) -> None:
    """TC-003: even a correct match fails while the OS lockout holds."""
    for _ in range(MAX_ATTEMPTS):
        with pytest.raises(BiometricAuthError):
            service.authenticate("wrong-finger")
    with pytest.raises(BiometricAuthError) as exc:
        service.authenticate("finger-1")
    assert exc.value.error is BiometricError.LOCKOUT


def test_second_lockout_becomes_permanent(service: BiometricAuthService) -> None:
    """TC-003: a second lockout cycle escalates to LOCKOUT_PERMANENT."""
    for _ in range(MAX_ATTEMPTS):
        with pytest.raises(BiometricAuthError):
            service.authenticate("wrong-finger")
    service.authenticate_with_passcode("123456")
    for _ in range(MAX_ATTEMPTS - 1):
        with pytest.raises(BiometricAuthError):
            service.authenticate("wrong-finger")
    with pytest.raises(BiometricAuthError) as exc:
        service.authenticate("wrong-finger")
    assert exc.value.error is BiometricError.LOCKOUT_PERMANENT
    with pytest.raises(BiometricAuthError) as exc2:
        service.authenticate("finger-1")
    assert exc2.value.error is BiometricError.LOCKOUT_PERMANENT


def test_enrollment_change_invalidates_credential(
    service: BiometricAuthService, device: Device
) -> None:
    """TC-004: a key bound to the enrolled set dies when the set changes."""
    service.store_credential()
    service.authenticate("finger-1")
    device.remove_all_biometrics()
    device.enroll("finger-2")
    assert service.credential_invalidated()
    with pytest.raises(BiometricAuthError) as exc:
        service.authenticate("finger-2")
    assert exc.value.error is BiometricError.KEY_INVALIDATED


def test_reenroll_after_invalidated_credential(
    service: BiometricAuthService, device: Device
) -> None:
    """TC-004: storing a fresh credential restores biometric login."""
    service.store_credential()
    device.remove_all_biometrics()
    service.reenroll_and_store("finger-2")
    session = service.authenticate("finger-2")
    assert session.method == "biometric"


def test_backgrounding_during_prompt_returns_to_login(
    service: BiometricAuthService,
) -> None:
    """TC-005: backgrounding cancels the prompt; no session, no crash."""
    service.begin_prompt()
    with pytest.raises(BiometricAuthError) as exc:
        service.cancel_prompt()
    assert exc.value.error is BiometricError.USER_CANCEL


def test_no_device_security_hides_biometric(device: Device, clock: FakeClock) -> None:
    """TC-006: without a passcode there is no strong authenticator."""
    device.passcode_set = False
    service = BiometricAuthService(device, clock)
    assert service.can_authenticate() is AuthenticatorClass.NONE
    with pytest.raises(BiometricAuthError) as exc:
        service.authenticate("finger-1")
    assert exc.value.error is BiometricError.DEVICE_SECURITY_REQUIRED


def test_no_sensor_reports_no_hardware(device: Device, clock: FakeClock) -> None:
    """Edge: a device without biometric hardware reports NONE."""
    device.has_sensor = False
    service = BiometricAuthService(device, clock)
    assert service.can_authenticate() is AuthenticatorClass.NONE
    with pytest.raises(BiometricAuthError) as exc:
        service.authenticate("finger-1")
    assert exc.value.error is BiometricError.NO_HARDWARE


def test_session_expiry_requires_reauth(
    service: BiometricAuthService, clock: FakeClock
) -> None:
    """TC-007: a session older than the timeout is no longer valid."""
    session = service.authenticate("finger-1")
    clock.advance(20 * 60)
    assert not service.is_session_valid(session.token)


def test_rooted_device_blocks_biometric(device: Device, clock: FakeClock) -> None:
    """TC-008: rooted devices get no biometric token."""
    device.rooted = True
    service = BiometricAuthService(device, clock)
    with pytest.raises(BiometricAuthError) as exc:
        service.authenticate("finger-1")
    assert exc.value.error is BiometricError.COMPROMISED_DEVICE


def test_device_credential_fallback(service: BiometricAuthService) -> None:
    """TC-009: device passcode issues an equivalent session and clears lockout."""
    for _ in range(MAX_ATTEMPTS):
        with pytest.raises(BiometricAuthError):
            service.authenticate("wrong-finger")
    session = service.authenticate_with_passcode("123456")
    assert session.method == "device_credential"
    assert service.is_session_valid(session.token)
    # lockout cleared: biometrics honored again
    assert service.authenticate("finger-1").method == "biometric"


def test_wrong_passcode_does_not_clear_lockout(
    service: BiometricAuthService,
) -> None:
    """TC-009: a wrong device credential keeps the lockout in place."""
    for _ in range(MAX_ATTEMPTS):
        with pytest.raises(BiometricAuthError):
            service.authenticate("wrong-finger")
    with pytest.raises(BiometricAuthError):
        service.authenticate_with_passcode("000000")
    with pytest.raises(BiometricAuthError) as exc:
        service.authenticate("finger-1")
    assert exc.value.error is BiometricError.LOCKOUT


def test_user_cancel_no_retry_loop(service: BiometricAuthService) -> None:
    """TC-010: cancelling returns to login and does not burn attempts."""
    for _ in range(3):
        with pytest.raises(BiometricAuthError) as exc:
            service.cancel_prompt()
        assert exc.value.error is BiometricError.USER_CANCEL
    # cancel attempts do not count as failures
    session = service.authenticate("finger-1")
    assert session.method == "biometric"


def test_prompt_timeout(service: BiometricAuthService) -> None:
    """Edge: an idle prompt raises TIMEOUT and the app stays on login."""
    with pytest.raises(BiometricAuthError) as exc:
        service.prompt_timeout()
    assert exc.value.error is BiometricError.TIMEOUT
