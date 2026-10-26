"""Tests for the WebAuthn ceremony simulator — mapped to TC-014 and the
ceremony-timeout edge case in the QAPractices 2FA test cases resource."""

import pytest

from webauthn_service import WebAuthnError, WebAuthnService

RP_ID = "staging.urbanthreads.com"
NOW = 1_700_000_000


@pytest.fixture
def webauthn():
    return WebAuthnService(rp_id=RP_ID, rp_name="UrbanThreads")


def enroll_key(webauthn, account="alice", now=NOW):
    options = webauthn.start_enrollment(account, "YubiKey 5 NFC", now=now)
    return webauthn.finish_enrollment(options["challenge_id"], origin=RP_ID, now=now)


def test_tc014_enrollment_returns_challenge_and_registers(webauthn):
    options = webauthn.start_enrollment("alice", "YubiKey 5 NFC", now=NOW)
    assert options["status"] == "pending_verification"
    assert options["rp"]["id"] == RP_ID
    credential_id = webauthn.finish_enrollment(
        options["challenge_id"], origin=RP_ID, now=NOW
    )
    assert credential_id.startswith("cred_")


def test_tc014_assertion_with_key_authenticates(webauthn):
    credential_id = enroll_key(webauthn)
    options = webauthn.start_assertion("alice", now=NOW)
    result = webauthn.finish_assertion(
        options["challenge_id"], credential_id, origin=RP_ID, now=NOW
    )
    assert result["status"] == "verified"
    assert result["method"] == "webauthn"
    assert result["session_id"].startswith("sess_")


def test_tc014_assertion_from_wrong_origin_rejected(webauthn):
    credential_id = enroll_key(webauthn)
    options = webauthn.start_assertion("alice", now=NOW)
    with pytest.raises(WebAuthnError, match="origin"):
        webauthn.finish_assertion(
            options["challenge_id"],
            credential_id,
            origin="staging-urbanthreads.com",
            now=NOW,
        )


def test_tc014_revoked_key_cannot_authenticate(webauthn):
    credential_id = enroll_key(webauthn)
    webauthn.revoke_credential("alice", credential_id)
    options = webauthn.start_assertion("alice", now=NOW)
    with pytest.raises(WebAuthnError, match="revoked"):
        webauthn.finish_assertion(
            options["challenge_id"], credential_id, origin=RP_ID, now=NOW
        )


def test_edge_ceremony_timeout_rejects_late_challenge(webauthn):
    options = webauthn.start_enrollment("alice", "YubiKey 5 NFC", now=NOW)
    with pytest.raises(WebAuthnError, match="expired"):
        webauthn.finish_enrollment(
            options["challenge_id"], origin=RP_ID, now=NOW + 61
        )


def test_edge_challenge_is_single_use(webauthn):
    options = webauthn.start_enrollment("alice", "YubiKey 5 NFC", now=NOW)
    webauthn.finish_enrollment(options["challenge_id"], origin=RP_ID, now=NOW)
    with pytest.raises(WebAuthnError, match="consumed"):
        webauthn.finish_enrollment(options["challenge_id"], origin=RP_ID, now=NOW)
