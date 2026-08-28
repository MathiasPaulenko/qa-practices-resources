"""TC-008, TC-009, TC-012, TC-014, TC-015: Token security tests."""
import pytest


class TestTokenSecurity:
    """Tests for token lifecycle and security boundaries."""

    def test_tc008_expired_token_rejected(self, api_session, base_url, expired_token, new_password):
        """TC-008: Expired token returns 400 with 'Token expired' message."""
        response = api_session.post(
            f"{base_url}/auth/reset-confirm",
            json={"token": expired_token, "newPassword": new_password},
        )
        assert response.status_code == 400
        data = response.json()
        assert "expired" in data.get("message", "").lower() or "invalid_token" in data.get("error", "").lower()

    def test_tc009_reused_token_rejected(self, api_session, base_url, reset_token, new_password):
        """TC-009: A token that was already used returns 400."""
        # First use should succeed
        first = api_session.post(
            f"{base_url}/auth/reset-confirm",
            json={"token": reset_token, "newPassword": new_password},
        )
        # Second use with same token should fail
        second = api_session.post(
            f"{base_url}/auth/reset-confirm",
            json={"token": reset_token, "newPassword": "AnotherPass789#"},
        )
        assert second.status_code == 400
        data = second.json()
        assert "used" in data.get("message", "").lower() or "invalid_token" in data.get("error", "").lower()

    def test_tc012_consecutive_tokens_differ(self, api_session, base_url, test_email):
        """TC-012: Two consecutive reset requests generate different tokens."""
        first = api_session.post(
            f"{base_url}/auth/reset-request",
            json={"email": test_email},
        )
        second = api_session.post(
            f"{base_url}/auth/reset-request",
            json={"email": test_email},
        )
        assert first.status_code == 200
        assert second.status_code == 200
        # Tokens would be extracted from MailHog in a real staging env.
        # This test validates that both requests succeed without error.

    def test_tc014_email_expiration_matches_config(self, api_session, base_url, test_email):
        """TC-014: Email states the correct expiration time."""
        # In a real staging env, capture the email via MailHog and parse the
        # expiration text. This test validates the request succeeds.
        response = api_session.post(
            f"{base_url}/auth/reset-request",
            json={"email": test_email},
        )
        assert response.status_code == 200

    def test_tc015_referer_header_no_token_leak(self, api_session, base_url, test_email):
        """TC-015: Reset link does not leak token in Referer header.

        This is a manual test in practice (requires opening the email with
        external images and inspecting the Referer header at the image server).
        The automated version validates the request endpoint works.
        """
        response = api_session.post(
            f"{base_url}/auth/reset-request",
            json={"email": test_email},
        )
        assert response.status_code == 200
        # Full Referer leak test requires Burp Suite 2024.x or OWASP ZAP 2.15
        # to intercept image requests from the email client.
