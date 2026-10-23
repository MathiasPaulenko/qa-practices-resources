"""Tests for the TOTP service — mapped to the TC-### cases in the
QAPractices Two-Factor Authentication test cases resource."""

import pytest

from totp_service import TOTPService

SECRET = "JBSWY3DPEHPK3PXP"
NOW = 1_700_000_000


@pytest.fixture
def svc():
    return TOTPService()


def test_tc002_valid_totp_code_authenticates(svc):
    code = svc.current_code(SECRET, at=NOW)
    assert svc.verify(SECRET, code, account="alice", at=NOW) is True


def test_tc003_wrong_code_rejected(svc):
    assert svc.verify(SECRET, "000000", account="alice", at=NOW) is False


def test_tc003_replayed_code_rejected(svc):
    code = svc.current_code(SECRET, at=NOW)
    assert svc.verify(SECRET, code, account="alice", at=NOW) is True
    assert svc.verify(SECRET, code, account="alice", at=NOW) is False


def test_tc003_expired_code_rejected(svc):
    code = svc.current_code(SECRET, at=NOW - 60)
    assert svc.verify(SECRET, code, account="alice", at=NOW) is False


def test_tc003_previous_window_rejected_with_zero_drift(svc):
    code = svc.current_code(SECRET, at=NOW - 30)
    assert svc.verify(SECRET, code, account="alice", at=NOW) is False


def test_tc009_one_step_drift_accepted_when_configured():
    svc = TOTPService(drift=1)
    code = svc.current_code(SECRET, at=NOW - 30)
    assert svc.verify(SECRET, code, account="alice", at=NOW) is True


def test_tc007_lockout_after_max_attempts(svc):
    for _ in range(5):
        svc.verify(SECRET, "111111", account="alice", at=NOW)
    assert svc.is_locked("alice")
    code = svc.current_code(SECRET, at=NOW)
    assert svc.verify(SECRET, code, account="alice", at=NOW) is False


def test_tc007_attempts_reset_after_success(svc):
    svc.verify(SECRET, "111111", account="alice", at=NOW)
    code = svc.current_code(SECRET, at=NOW)
    assert svc.verify(SECRET, code, account="alice", at=NOW) is True
    assert not svc.is_locked("alice")


def test_tc006_backup_code_works_once(svc):
    codes = svc.issue_backup_codes("alice")
    code = codes[0]
    assert svc.verify_backup_code("alice", code) is True
    assert svc.verify_backup_code("alice", code) is False


def test_tc006_backup_code_exhaustion(svc):
    codes = svc.issue_backup_codes("alice", count=3)
    for c in codes:
        assert svc.verify_backup_code("alice", c) is True
    assert svc.remaining_backup_codes("alice") == 0
    assert svc.verify_backup_code("alice", codes[0]) is False


def test_tc001_secret_has_at_least_128_bits(svc):
    import base64

    secret = svc.generate_secret("alice@example.com")
    raw = base64.b32decode(secret + "=" * (-len(secret) % 8))
    assert len(raw) >= 16
