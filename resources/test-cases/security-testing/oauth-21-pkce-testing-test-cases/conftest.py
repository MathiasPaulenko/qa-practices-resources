"""Pytest fixtures for OAuth 2.1 PKCE test cases."""

import pytest

from mock_auth_server import MockAuthServer
from pkce_utils import generate_pkce_pair, generate_plain_challenge


@pytest.fixture
def auth_server():
    """Fresh mock authorization server for each test."""
    return MockAuthServer(code_ttl=600)


@pytest.fixture
def auth_server_short_ttl():
    """Mock auth server with 1-second TTL for expiry tests."""
    return MockAuthServer(code_ttl=1)


@pytest.fixture
def pkce_pair():
    """Valid S256 PKCE pair."""
    return generate_pkce_pair()


@pytest.fixture
def plain_pair():
    """Plain PKCE pair (should be rejected by OAuth 2.1 servers)."""
    return generate_plain_challenge()


@pytest.fixture
def client_config():
    """Standard client configuration for tests."""
    return {
        "client_id": "pkce-client",
        "redirect_uri": "https://client.qapractices/callback",
        "scope": "openid profile",
    }
