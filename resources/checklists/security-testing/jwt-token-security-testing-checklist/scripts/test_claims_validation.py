"""Test exp, iss, aud, iat claim validation."""
import time
import pytest
import jwt
from cryptography.hazmat.primitives import serialization

with open("private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())


def test_wrong_audience_rejected():
    payload = {"sub": "user-123", "aud": "other-api", "exp": time.time() + 300}
    token = jwt.encode(payload, private_key, algorithm="RS256")
    with pytest.raises(jwt.InvalidAudienceError):
        jwt.decode(token, public_key, algorithms=["RS256"], audience="checkout-api")


def test_wrong_issuer_rejected():
    payload = {"sub": "user-123", "iss": "https://evil.com", "exp": time.time() + 300}
    token = jwt.encode(payload, private_key, algorithm="RS256")
    with pytest.raises(jwt.InvalidIssuerError):
        jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer="https://auth.qa.local",
        )


def test_future_iat_rejected():
    payload = {
        "sub": "user-123",
        "iat": time.time() + 120,
        "exp": time.time() + 300,
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    with pytest.raises(jwt.ImmatureSignatureError):
        jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"require": ["iat"]},
            leeway=60,
        )
