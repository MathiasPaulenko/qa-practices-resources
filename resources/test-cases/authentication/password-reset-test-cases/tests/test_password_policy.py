"""TC-003, TC-010: Password policy enforcement during reset."""
import pytest


class TestPasswordPolicy:
    """Tests for password policy validation during reset."""

    def test_tc003_weak_password_rejected(self, api_session, base_url, reset_token, weak_password):
        """TC-003: Weak password returns 400 with policy error."""
        response = api_session.post(
            f"{base_url}/auth/reset-confirm",
            json={"token": reset_token, "newPassword": weak_password},
        )
        assert response.status_code == 400
        data = response.json()
        message = data.get("message", "").lower()
        assert "length" in message or "policy" in message or "weak" in message

    def test_tc010_recently_used_password_rejected(self, api_session, base_url, reset_token):
        """TC-010: A password matching one of the last 5 is rejected."""
        # Use a password that should be in history (replace with a real
        # historical password from your staging DB).
        recent_password = "SecurePass123!"
        response = api_session.post(
            f"{base_url}/auth/reset-confirm",
            json={"token": reset_token, "newPassword": recent_password},
        )
        assert response.status_code == 400
        data = response.json()
        message = data.get("message", "").lower()
        assert "recently" in message or "history" in message or "used" in message
