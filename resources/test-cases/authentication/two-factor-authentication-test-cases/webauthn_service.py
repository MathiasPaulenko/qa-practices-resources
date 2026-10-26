"""Minimal WebAuthn ceremony simulator for the 2FA test cases companion.

Models the server side of FIDO2/WebAuthn ceremonies — challenge issuance
with a 60-second TTL, single-use challenges, origin binding, credential
registration and revocation — so the TC-014 cases (enrollment, assertion,
wrong-origin rejection, revocation, ceremony timeout) run without a real
authenticator. This is not real attestation crypto: the `attestation` and
`assertion` payloads stand in for signed authenticator responses; what
matters for the test cases is the ceremony state machine.
"""

import secrets
import time


class WebAuthnError(Exception):
    """Raised when a ceremony step fails validation."""


class WebAuthnService:
    CHALLENGE_TTL = 60  # seconds — matches the ceremony-timeout edge case

    def __init__(self, rp_id, rp_name="QAPractices"):
        self.rp_id = rp_id
        self.rp_name = rp_name
        self._challenges = {}
        self._credentials = {}

    def start_enrollment(self, account, device_name, now=None):
        """Returns a PublicKeyCredentialCreationOptions-style payload."""
        challenge_id = self._issue_challenge(account, "enrollment", now, device_name)
        return {
            "status": "pending_verification",
            "challenge_id": challenge_id,
            "challenge": secrets.token_urlsafe(24),
            "rp": {"name": self.rp_name, "id": self.rp_id},
            "user": {"id": account, "name": account},
            "device_name": device_name,
        }

    def finish_enrollment(self, challenge_id, origin, attestation="attest", now=None):
        """Completes registration; returns the new credential_id."""
        ch = self._consume_challenge(challenge_id, "enrollment", origin, now)
        credential_id = "cred_" + secrets.token_hex(8)
        self._credentials.setdefault(ch["account"], {})[credential_id] = {
            "device": ch["device_name"],
            "revoked": False,
        }
        return credential_id

    def start_assertion(self, account, now=None):
        """Returns a PublicKeyCredentialRequestOptions-style payload."""
        challenge_id = self._issue_challenge(account, "assertion", now)
        return {
            "status": "pending_verification",
            "challenge_id": challenge_id,
            "challenge": secrets.token_urlsafe(24),
            "rp": {"name": self.rp_name, "id": self.rp_id},
        }

    def finish_assertion(self, challenge_id, credential_id, origin, assertion="sig", now=None):
        """Completes authentication; returns a verified session payload."""
        ch = self._consume_challenge(challenge_id, "assertion", origin, now)
        cred = self._credentials.get(ch["account"], {}).get(credential_id)
        if cred is None or cred["revoked"]:
            raise WebAuthnError("credential unknown or revoked")
        return {
            "status": "verified",
            "method": "webauthn",
            "session_id": "sess_" + secrets.token_hex(4),
        }

    def revoke_credential(self, account, credential_id):
        cred = self._credentials.get(account, {}).get(credential_id)
        if cred is not None:
            cred["revoked"] = True

    def _issue_challenge(self, account, kind, now, device_name=None):
        now = time.time() if now is None else now
        challenge_id = secrets.token_urlsafe(16)
        self._challenges[challenge_id] = {
            "account": account,
            "kind": kind,
            "device_name": device_name,
            "expires_at": now + self.CHALLENGE_TTL,
            "used": False,
        }
        return challenge_id

    def _consume_challenge(self, challenge_id, kind, origin, now):
        ch = self._challenges.get(challenge_id)
        if ch is None or ch["used"]:
            raise WebAuthnError("unknown or consumed challenge")
        now = time.time() if now is None else now
        if now > ch["expires_at"]:
            raise WebAuthnError("challenge expired")
        if ch["kind"] != kind:
            raise WebAuthnError("challenge kind mismatch")
        if origin != self.rp_id:
            raise WebAuthnError("origin mismatch: credentials are origin-bound")
        ch["used"] = True
        return ch
