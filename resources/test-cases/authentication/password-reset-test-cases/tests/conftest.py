"""Shared fixtures and configuration for password reset test cases."""
import os
import pytest
import requests


BASE_URL = os.environ.get("BASE_URL", "https://demo-api.qapractices.test")
TEST_EMAIL = "qa-tester@qapractices.test"
UNKNOWN_EMAIL = "unknown@qapractices.test"
NEW_PASSWORD = "NewSecurePass456@"
WEAK_PASSWORD = "weak"
RESET_TOKEN = "reset-token-abc123xyz"
EXPIRED_TOKEN = "expired-token-xyz789"


@pytest.fixture
def api_session():
    """Requests session with default headers and timeout."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    session.timeout = 10
    return session


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def test_email():
    return TEST_EMAIL


@pytest.fixture
def unknown_email():
    return UNKNOWN_EMAIL


@pytest.fixture
def new_password():
    return NEW_PASSWORD


@pytest.fixture
def weak_password():
    return WEAK_PASSWORD


@pytest.fixture
def reset_token():
    return RESET_TOKEN


@pytest.fixture
def expired_token():
    return EXPIRED_TOKEN
