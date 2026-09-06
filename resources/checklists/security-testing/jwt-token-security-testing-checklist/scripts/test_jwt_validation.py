"""Test RS256 signature verification with PyJWT 2.10."""
import time
import pytest
import jwt
from cryptography.hazmat.primitives import serialization

with open("private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())


def test_rs256_signature_verified():
    payload = {
        "sub": "user-123",
        "iss": "https://auth.qa.local",
        "aud": "checkout-api",
        "iat": time.time(),
        "exp": time.time() + 300,
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience="checkout-api",
        issuer="https://auth.qa.local",
    )
    assert decoded["sub"] == "user-123"
    assert decoded["exp"] > time.time()


def test_expired_token_rejected():
    payload = {
        "sub": "user-123",
        "exp": time.time() - 10,
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, public_key, algorithms=["RS256"])
