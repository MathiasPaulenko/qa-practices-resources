"""Test that modified payloads with tampered signatures are rejected."""
import time
import json
import base64
import pytest
import jwt
from cryptography.hazmat.primitives import serialization

with open("private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())


def test_tampered_payload_rejected():
    payload = {
        "sub": "user-123",
        "role": "user",
        "exp": time.time() + 300,
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")

    parts = token.split(".")
    decoded_payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=="))
    decoded_payload["role"] = "admin"
    tampered_payload = base64.urlsafe_b64encode(
        json.dumps(decoded_payload).encode()
    ).rstrip(b"=").decode()
    tampered_token = parts[0] + "." + tampered_payload + "." + parts[2]

    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(tampered_token, public_key, algorithms=["RS256"])
