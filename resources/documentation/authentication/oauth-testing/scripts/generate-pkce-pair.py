"""Generate PKCE code_verifier and code_challenge (S256).

Usage: python generate-pkce-pair.py
Requires: Python 3.10+, no external dependencies.
"""
import base64
import hashlib
import secrets


def generate_pkce_pair():
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("utf-8").rstrip("=")
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("utf-8")).digest()
    ).decode("utf-8").rstrip("=")
    return verifier, challenge


if __name__ == "__main__":
    v, c = generate_pkce_pair()
    print(f"code_verifier:  {v}")
    print(f"code_challenge: {c}")
    print(f"method:         S256")
