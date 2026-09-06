"""Test that alg:none and RS256->HS256 algorithm confusion are rejected."""
import pytest
import jwt
from cryptography.hazmat.primitives import serialization

with open("private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())


def test_none_algorithm_rejected():
    none_token = jwt.encode({"sub": "user-123"}, None, algorithm="none")
    with pytest.raises(jwt.InvalidAlgorithmError):
        jwt.decode(none_token, public_key, algorithms=["RS256"])


def test_algorithm_confusion_rejected():
    token = jwt.encode({"sub": "user-123"}, key="public-key-as-secret", algorithm="HS256")
    with pytest.raises((jwt.InvalidAlgorithmError, jwt.InvalidKeyError)):
        jwt.decode(token, public_key, algorithms=["RS256"])
