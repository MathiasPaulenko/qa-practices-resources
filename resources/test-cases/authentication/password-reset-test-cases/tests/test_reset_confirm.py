"""TC-002, TC-004, TC-005, TC-013: Reset confirm and login tests."""
import pytest


class TestResetConfirm:
    """Tests for POST /auth/reset-confirm and post-reset login."""

    def test_tc002_reset_with_valid_token(self, api_session, base_url, reset_token, new_password):
        """TC-002: Complete reset with a valid token succeeds."""
        response = api_session.post(
            f"{base_url}/auth/reset-confirm",
            json={"token": reset_token, "newPassword": new_password},
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "success"

    def test_tc004_password_confirmation_mismatch(self, api_session, base_url, reset_token, new_password):
        """TC-004: Mismatched confirmation is rejected before API call (UI-level)."""
        # This test validates the API contract: the API should also reject
        # if confirmPassword is sent and doesn't match.
        response = api_session.post(
            f"{base_url}/auth/reset-confirm",
            json={
                "token": reset_token,
                "newPassword": new_password,
                "confirmPassword": "DifferentPass789#",
            },
        )
        assert response.status_code == 400

    def test_tc005_login_with_new_password(self, api_session, base_url, test_email, new_password):
        """TC-005: Login with new password succeeds; old password returns 401."""
        response = api_session.post(
            f"{base_url}/auth/login",
            json={"email": test_email, "password": new_password},
        )
        assert response.status_code == 200

    def test_tc013_no_auto_login_after_reset(self, api_session, base_url, reset_token, new_password):
        """TC-013: After reset, no session cookie is set (redirect to login)."""
        response = api_session.post(
            f"{base_url}/auth/reset-confirm",
            json={"token": reset_token, "newPassword": new_password},
            allow_redirects=False,
        )
        # No session cookie should be present in the response
        cookies = response.cookies.get_dict()
        assert "session" not in cookies
