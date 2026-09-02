"""Mock authorization server for OAuth 2.1 PKCE test cases.

Simulates an OAuth 2.1 compliant authorization server with:
- S256-only PKCE enforcement
- Authorization code lifecycle (10 min TTL)
- Refresh token rotation
- Scope enforcement
- State parameter validation
"""

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AuthorizationCode:
    code: str
    client_id: str
    redirect_uri: str
    code_challenge: str
    code_challenge_method: str
    scope: str
    state: str
    created_at: float = field(default_factory=time.time)
    ttl: int = 600  # 10 minutes
    used: bool = False


@dataclass
class RefreshToken:
    token: str
    client_id: str
    scope: str
    rotated: bool = False


class MockAuthServer:
    """In-memory mock of an OAuth 2.1 authorization server."""

    def __init__(self, code_ttl: int = 600):
        self.codes: dict[str, AuthorizationCode] = {}
        self.refresh_tokens: dict[str, RefreshToken] = {}
        self.access_tokens: dict[str, dict] = {}
        self.code_ttl = code_ttl
        self._counter = 0

    def _next_id(self, prefix: str = "id") -> str:
        self._counter += 1
        return f"{prefix}-{self._counter:04d}"

    def authorize(
        self,
        client_id: str,
        redirect_uri: str,
        code_challenge: str,
        code_challenge_method: str,
        scope: str = "",
        state: str = "",
    ) -> str:
        """Process an authorization request. Returns the code or raises ValueError."""
        if not code_challenge:
            raise ValueError("invalid_request: code_challenge is required")
        if code_challenge_method != "S256":
            raise ValueError(
                "invalid_request: only S256 code_challenge_method is allowed"
            )
        code = self._next_id("code")
        self.codes[code] = AuthorizationCode(
            code=code,
            client_id=client_id,
            redirect_uri=redirect_uri,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            scope=scope,
            state=state,
            ttl=self.code_ttl,
        )
        return code

    def exchange_code(
        self,
        code: str,
        code_verifier: str,
        client_id: str,
        redirect_uri: str,
    ) -> dict:
        """Exchange an authorization code for tokens. Returns token dict or raises."""
        if code not in self.codes:
            raise ValueError("invalid_grant: unknown authorization code")

        ac = self.codes[code]

        if ac.used:
            raise ValueError("invalid_grant: authorization code already used")

        if time.time() - ac.created_at > ac.ttl:
            raise ValueError("invalid_grant: authorization code expired")

        if ac.redirect_uri != redirect_uri:
            raise ValueError("invalid_redirect_uri: redirect URI mismatch")

        if ac.client_id != client_id:
            raise ValueError("invalid_client: client_id mismatch")

        # Verify PKCE
        import base64
        import hashlib

        expected_challenge = (
            base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode("ascii")).digest()
            )
            .rstrip(b"=")
            .decode("ascii")
        )
        if expected_challenge != ac.code_challenge:
            raise ValueError(
                "invalid_grant: code_verifier does not match code_challenge"
            )

        # Mark code as used
        ac.used = True

        # Issue tokens
        access_token = self._next_id("at")
        refresh_token = self._next_id("rt")
        self.access_tokens[access_token] = {
            "client_id": client_id,
            "scope": ac.scope,
        }
        self.refresh_tokens[refresh_token] = RefreshToken(
            token=refresh_token, client_id=client_id, scope=ac.scope
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": ac.scope,
        }

    def refresh(self, refresh_token: str) -> dict:
        """Use a refresh token to get a new access token. Implements rotation."""
        if refresh_token not in self.refresh_tokens:
            raise ValueError("invalid_grant: unknown refresh token")

        rt = self.refresh_tokens[refresh_token]
        if rt.rotated:
            raise ValueError(
                "invalid_grant: refresh token already rotated (reuse detected)"
            )

        # Rotate: invalidate old, issue new
        rt.rotated = True
        new_access = self._next_id("at")
        new_refresh = self._next_id("rt")
        self.access_tokens[new_access] = {
            "client_id": rt.client_id,
            "scope": rt.scope,
        }
        self.refresh_tokens[new_refresh] = RefreshToken(
            token=new_refresh, client_id=rt.client_id, scope=rt.scope
        )

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": rt.scope,
        }

    def validate_scope(self, access_token: str, required_scope: str) -> bool:
        """Check if an access token has the required scope."""
        if access_token not in self.access_tokens:
            return False
        granted = self.access_tokens[access_token]["scope"].split()
        return required_scope in granted
