"""Tests for the login gateway — mapped to TC-015 (server-side bypass
attempts) and TC-016 (2FA enforcement for privileged roles) in the
QAPractices 2FA test cases resource."""

import pytest

from login_gateway import LoginGateway
from totp_service import TOTPService

SECRET = "JBSWY3DPEHPK3PXP"
OTHER_SECRET = "KRSXG5DSN5ZGK3TFOJ4Q"


@pytest.fixture
def gateway():
    totp = TOTPService()
    gw = LoginGateway(totp=totp)
    gw.add_user("alice", "s3cret-pass", role="user", totp_secret=SECRET)
    gw.add_user("bob", "s3cret-pass", role="user")
    gw.add_user("root", "s3cret-pass", role="admin")
    return gw


def test_tc015_login_returns_pre_auth_state_not_session(gateway):
    result = gateway.login("alice", "s3cret-pass")
    assert result["2fa_required"] is True
    assert "pre_auth_token" in result
    assert "session_token" not in result


def test_tc015_injected_client_flags_ignored(gateway):
    result = gateway.login("alice", "s3cret-pass", **{
        "2fa_verified": True,
        "skip_2fa": True,
    })
    assert result["2fa_required"] is True
    assert "session_token" not in result


def test_tc015_pre_auth_token_cannot_reach_account(gateway):
    token = gateway.login("alice", "s3cret-pass")["pre_auth_token"]
    assert gateway.get_account(token)["status"] == 401


def test_tc015_code_bound_to_requesting_account(gateway):
    token = gateway.login("alice", "s3cret-pass")["pre_auth_token"]
    other_code = gateway.totp.current_code(OTHER_SECRET)
    assert gateway.verify_2fa(token, other_code)["status"] == 401


def test_tc015_full_flow_issues_session(gateway):
    token = gateway.login("alice", "s3cret-pass")["pre_auth_token"]
    code = gateway.totp.current_code(SECRET)
    result = gateway.verify_2fa(token, code)
    assert result["status"] == 200
    assert gateway.get_account(result["session_token"])["user"] == "alice"


def test_tc016_admin_without_2fa_blocked_from_admin_surface(gateway):
    result = gateway.login("root", "s3cret-pass")
    assert "2fa_enrollment_required" in result["flags"]
    denied = gateway.admin_access(result["session_token"])
    assert denied["status"] == 403
    assert denied["error"] == "2fa_enrollment_required"


def test_tc016_admin_gains_access_after_enrolling(gateway):
    gateway._users["root"]["totp_secret"] = SECRET
    token = gateway.login("root", "s3cret-pass")["pre_auth_token"]
    code = gateway.totp.current_code(SECRET)
    session = gateway.verify_2fa(token, code)["session_token"]
    assert gateway.admin_access(session)["status"] == 200


def test_tc016_control_user_keeps_normal_surfaces(gateway):
    result = gateway.login("bob", "s3cret-pass")
    assert gateway.get_account(result["session_token"])["status"] == 200
    assert gateway.admin_access(result["session_token"])["status"] == 403
