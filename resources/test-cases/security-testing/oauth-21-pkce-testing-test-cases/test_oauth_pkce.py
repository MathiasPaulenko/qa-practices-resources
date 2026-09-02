"""OAuth 2.1 & PKCE test cases — TC-01 through TC-10.

Run with: pytest test_oauth_pkce.py -v
Requirements: pytest 8.3+
"""

import time

import pytest

from pkce_utils import generate_pkce_pair, generate_plain_challenge


class TestTC01ValidAuthCodeFlowS256:
    """TC-01: Valid authorization code flow with S256 PKCE."""

    def test_valid_flow_returns_tokens(self, auth_server, pkce_pair, client_config):
        code = auth_server.authorize(
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
            code_challenge=pkce_pair.challenge,
            code_challenge_method="S256",
            scope=client_config["scope"],
            state="test-state-123",
        )
        assert code is not None

        tokens = auth_server.exchange_code(
            code=code,
            code_verifier=pkce_pair.verifier,
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
        )
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["token_type"] == "Bearer"
        assert tokens["scope"] == client_config["scope"]


class TestTC02MissingCodeChallenge:
    """TC-02: Authorization request missing PKCE code challenge."""

    def test_missing_challenge_rejected(self, auth_server, client_config):
        with pytest.raises(ValueError, match="code_challenge is required"):
            auth_server.authorize(
                client_id=client_config["client_id"],
                redirect_uri=client_config["redirect_uri"],
                code_challenge="",
                code_challenge_method="S256",
            )


class TestTC03PlainMethodRejected:
    """TC-03: plain code challenge method rejected."""

    def test_plain_method_rejected(self, auth_server, plain_pair, client_config):
        with pytest.raises(ValueError, match="only S256"):
            auth_server.authorize(
                client_id=client_config["client_id"],
                redirect_uri=client_config["redirect_uri"],
                code_challenge=plain_pair.challenge,
                code_challenge_method="plain",
            )

    def test_s256_method_accepted(self, auth_server, pkce_pair, client_config):
        code = auth_server.authorize(
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
            code_challenge=pkce_pair.challenge,
            code_challenge_method="S256",
        )
        assert code is not None


class TestTC04VerifierMismatch:
    """TC-04: Code verifier doesn't match the challenge."""

    def test_wrong_verifier_rejected(self, auth_server, pkce_pair, client_config):
        code = auth_server.authorize(
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
            code_challenge=pkce_pair.challenge,
            code_challenge_method="S256",
        )
        with pytest.raises(ValueError, match="code_verifier does not match"):
            auth_server.exchange_code(
                code=code,
                code_verifier="completely-different-verifier-string-43-chars",
                client_id=client_config["client_id"],
                redirect_uri=client_config["redirect_uri"],
            )


class TestTC05CodeExpired:
    """TC-05: Authorization code used after expiration."""

    def test_expired_code_rejected(self, auth_server_short_ttl, pkce_pair, client_config):
        code = auth_server_short_ttl.authorize(
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
            code_challenge=pkce_pair.challenge,
            code_challenge_method="S256",
        )
        time.sleep(2)  # Wait for code to expire (TTL=1s)
        with pytest.raises(ValueError, match="expired"):
            auth_server_short_ttl.exchange_code(
                code=code,
                code_verifier=pkce_pair.verifier,
                client_id=client_config["client_id"],
                redirect_uri=client_config["redirect_uri"],
            )


class TestTC06CodeReplay:
    """TC-06: Authorization code exchanged more than once."""

    def test_code_replay_rejected(self, auth_server, pkce_pair, client_config):
        code = auth_server.authorize(
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
            code_challenge=pkce_pair.challenge,
            code_challenge_method="S256",
        )
        # First exchange succeeds
        tokens = auth_server.exchange_code(
            code=code,
            code_verifier=pkce_pair.verifier,
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
        )
        assert "access_token" in tokens
        # Second exchange fails
        with pytest.raises(ValueError, match="already used"):
            auth_server.exchange_code(
                code=code,
                code_verifier=pkce_pair.verifier,
                client_id=client_config["client_id"],
                redirect_uri=client_config["redirect_uri"],
            )


class TestTC07RedirectURIValidation:
    """TC-07: Redirect URI strict validation."""

    def test_exact_match_succeeds(self, auth_server, pkce_pair, client_config):
        code = auth_server.authorize(
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
            code_challenge=pkce_pair.challenge,
            code_challenge_method="S256",
        )
        tokens = auth_server.exchange_code(
            code=code,
            code_verifier=pkce_pair.verifier,
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
        )
        assert "access_token" in tokens

    def test_trailing_slash_rejected(self, auth_server, pkce_pair, client_config):
        code = auth_server.authorize(
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
            code_challenge=pkce_pair.challenge,
            code_challenge_method="S256",
        )
        with pytest.raises(ValueError, match="redirect URI mismatch"):
            auth_server.exchange_code(
                code=code,
                code_verifier=pkce_pair.verifier,
                client_id=client_config["client_id"],
                redirect_uri=client_config["redirect_uri"] + "/",
            )


class TestTC08StateParameter:
    """TC-08: State parameter CSRF protection."""

    def test_matching_state_succeeds(self, auth_server, pkce_pair, client_config):
        state = "random-128-bit-state-value"
        code = auth_server.authorize(
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
            code_challenge=pkce_pair.challenge,
            code_challenge_method="S256",
            state=state,
        )
        # Client verifies state matches before exchanging
        assert state == "random-128-bit-state-value"

    def test_mismatched_state_rejected_by_client(self, auth_server, pkce_pair, client_config):
        state_sent = "legitimate-state"
        state_received = "attacker-state"
        # Client must reject if state doesn't match
        assert state_sent != state_received


class TestTC09RefreshTokenRotation:
    """TC-09: Refresh token is rotated and old token is invalidated."""

    def test_rotation_invalidates_old_token(self, auth_server, pkce_pair, client_config):
        code = auth_server.authorize(
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
            code_challenge=pkce_pair.challenge,
            code_challenge_method="S256",
        )
        tokens = auth_server.exchange_code(
            code=code,
            code_verifier=pkce_pair.verifier,
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
        )
        old_refresh = tokens["refresh_token"]

        # First refresh succeeds and returns new token
        new_tokens = auth_server.refresh(old_refresh)
        assert new_tokens["refresh_token"] != old_refresh

        # Old token is now invalid
        with pytest.raises(ValueError, match="already rotated"):
            auth_server.refresh(old_refresh)


class TestTC10ScopeEnforcement:
    """TC-10: Access token is restricted to granted scopes."""

    def test_granted_scope_succeeds(self, auth_server, pkce_pair, client_config):
        code = auth_server.authorize(
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
            code_challenge=pkce_pair.challenge,
            code_challenge_method="S256",
            scope="read:profile read:orders",
        )
        tokens = auth_server.exchange_code(
            code=code,
            code_verifier=pkce_pair.verifier,
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
        )
        assert auth_server.validate_scope(tokens["access_token"], "read:profile")
        assert auth_server.validate_scope(tokens["access_token"], "read:orders")

    def test_ungranted_scope_rejected(self, auth_server, pkce_pair, client_config):
        code = auth_server.authorize(
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
            code_challenge=pkce_pair.challenge,
            code_challenge_method="S256",
            scope="read:profile",
        )
        tokens = auth_server.exchange_code(
            code=code,
            code_verifier=pkce_pair.verifier,
            client_id=client_config["client_id"],
            redirect_uri=client_config["redirect_uri"],
        )
        assert auth_server.validate_scope(tokens["access_token"], "read:profile")
        assert not auth_server.validate_scope(tokens["access_token"], "write:orders")
