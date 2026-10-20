"""Minimal biometric auth policy model that mirrors the resource's rules.

Simulates the iOS LocalAuthentication / Android BiometricPrompt state machine:
match attempts, OS lockout after five failures, device credential fallback,
enrollment-change invalidation and session expiry. Not production code — a
test lab for the mobile-biometric-authentication-testing resource.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

MAX_ATTEMPTS = 5
LOCKOUTS_BEFORE_PERMANENT = 2
SESSION_TTL_S = 15 * 60


class BiometricError(Enum):
    """Platform error surface, mirroring LAError / BIOMETRIC_ERROR_*."""

    NO_HARDWARE = "no_hardware"
    NOT_ENROLLED = "not_enrolled"
    DEVICE_SECURITY_REQUIRED = "device_security_required"
    NO_MATCH = "no_match"
    LOCKOUT = "lockout"
    LOCKOUT_PERMANENT = "lockout_permanent"
    USER_CANCEL = "user_cancel"
    TIMEOUT = "timeout"
    COMPROMISED_DEVICE = "compromised_device"
    KEY_INVALIDATED = "key_invalidated"


class BiometricAuthError(Exception):
    def __init__(self, error: BiometricError) -> None:
        super().__init__(error.value)
        self.error = error


class AuthenticatorClass(Enum):
    NONE = "none"
    WEAK = "weak"
    STRONG = "strong"


@dataclass
class Device:
    """Hardware and OS-level biometric state."""

    has_sensor: bool = True
    passcode_set: bool = True
    rooted: bool = False
    enrolled: set[str] = field(default_factory=lambda: {"finger-1"})

    def enroll(self, biometric_id: str) -> None:
        self.enrolled.add(biometric_id)

    def remove_all_biometrics(self) -> None:
        self.enrolled.clear()


@dataclass
class Session:
    token: str
    issued_at: float
    expires_at: float
    method: str  # "biometric" | "device_credential" | "password"


class BiometricAuthService:
    """App-side biometric auth with the platform policy baked in."""

    def __init__(self, device: Device, now: Callable[[], float]) -> None:
        self.device = device
        self._now = now
        self._failed_attempts = 0
        self._lockout_cycles = 0
        self._locked = False
        self._permanent_lock = False
        self._enrolled_snapshot = set(device.enrolled)
        self._credential_valid = False
        self._sessions: dict[str, Session] = {}

    # --- capability check (BiometricManager.canAuthenticate / LAContext) ---

    def can_authenticate(self) -> AuthenticatorClass:
        if not self.device.has_sensor:
            return AuthenticatorClass.NONE
        if not self.device.passcode_set:
            return AuthenticatorClass.NONE
        if not self.device.enrolled:
            return AuthenticatorClass.WEAK
        return AuthenticatorClass.STRONG

    def biometric_option_visible(self) -> bool:
        """What the login screen shows before any prompt."""
        return self.can_authenticate() is AuthenticatorClass.STRONG

    # --- stored credential (Keychain biometryCurrentSet / Keystore flag) ---

    def store_credential(self) -> None:
        """App stores a key bound to the current biometric set."""
        self._credential_valid = True
        self._enrolled_snapshot = set(self.device.enrolled)

    def credential_invalidated(self) -> bool:
        """Keys bound to the enrolled set die when the set changes."""
        return self._credential_valid and self.device.enrolled != self._enrolled_snapshot

    # --- authentication ---

    def begin_prompt(self) -> None:
        """Show the system prompt; the attempt counter does not reset here."""
        if self.device.rooted:
            raise BiometricAuthError(BiometricError.COMPROMISED_DEVICE)
        if not self.device.has_sensor:
            raise BiometricAuthError(BiometricError.NO_HARDWARE)
        if not self.device.passcode_set:
            raise BiometricAuthError(BiometricError.DEVICE_SECURITY_REQUIRED)
        if not self.device.enrolled:
            raise BiometricAuthError(BiometricError.NOT_ENROLLED)
        if self._permanent_lock:
            raise BiometricAuthError(BiometricError.LOCKOUT_PERMANENT)
        if self._locked:
            raise BiometricAuthError(BiometricError.LOCKOUT)

    def cancel_prompt(self) -> None:
        """User/system cancel: app returns to login, no retry, no session."""
        raise BiometricAuthError(BiometricError.USER_CANCEL)

    def prompt_timeout(self) -> None:
        """Prompt idle past the ~30s system timeout."""
        raise BiometricAuthError(BiometricError.TIMEOUT)

    def authenticate(self, biometric_id: str) -> Session:
        self.begin_prompt()
        if self.credential_invalidated():
            raise BiometricAuthError(BiometricError.KEY_INVALIDATED)
        if biometric_id in self.device.enrolled:
            self._failed_attempts = 0
            return self._issue("biometric")
        self._failed_attempts += 1
        if self._failed_attempts >= MAX_ATTEMPTS:
            self._lockout_cycles += 1
            if self._lockout_cycles >= LOCKOUTS_BEFORE_PERMANENT:
                self._permanent_lock = True
                raise BiometricAuthError(BiometricError.LOCKOUT_PERMANENT)
            self._locked = True
            raise BiometricAuthError(BiometricError.LOCKOUT)
        raise BiometricAuthError(BiometricError.NO_MATCH)

    def authenticate_with_passcode(self, pin: str) -> Session:
        """Device credential fallback; a correct passcode clears lockout."""
        if pin != "123456":
            raise BiometricAuthError(BiometricError.NO_MATCH)
        self._failed_attempts = 0
        self._locked = False
        return self._issue("device_credential")

    def reenroll_and_store(self, biometric_id: str) -> None:
        """After re-auth the app stores a fresh credential for the new set."""
        self.device.enrolled = {biometric_id}
        self.store_credential()

    # --- sessions ---

    def _issue(self, method: str) -> Session:
        session = Session(
            token=secrets.token_hex(8),
            issued_at=self._now(),
            expires_at=self._now() + SESSION_TTL_S,
            method=method,
        )
        self._sessions[session.token] = session
        return session

    def is_session_valid(self, token: str) -> bool:
        session = self._sessions.get(token)
        return session is not None and session.expires_at > self._now()
