"""TC-001, TC-006, TC-007: Reset request endpoint tests."""
import pytest


class TestResetRequest:
    """Tests for POST /auth/reset-request."""

    def test_tc001_reset_request_with_valid_email(self, api_session, base_url, test_email):
        """TC-001: Request reset with a registered email returns generic message."""
        response = api_session.post(
            f"{base_url}/auth/reset-request",
            json={"email": test_email},
        )
        assert response.status_code == 200
        data = response.json()
        assert "account exists" in data.get("message", "").lower()

    def test_tc006_reset_request_with_unregistered_email(self, api_session, base_url, unknown_email):
        """TC-006: Unregistered email returns the same generic message (no enumeration)."""
        response = api_session.post(
            f"{base_url}/auth/reset-request",
            json={"email": unknown_email},
        )
        assert response.status_code == 200
        data = response.json()
        assert "account exists" in data.get("message", "").lower()

    def test_tc007_reset_request_with_invalid_email_format(self, api_session, base_url):
        """TC-007: Invalid email format returns 400 validation error."""
        response = api_session.post(
            f"{base_url}/auth/reset-request",
            json={"email": "not-an-email"},
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data or "validation" in data.get("message", "").lower()
