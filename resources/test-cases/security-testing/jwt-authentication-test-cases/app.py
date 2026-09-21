"""JWT lab for the JWT Authentication Test Cases resource.

A minimal Flask app that issues RS256 tokens and exposes two verification
styles:

- /secure/*     verifies correctly: the algorithm is pinned server-side,
                claims are checked on every request, and revoked jti values
                land on a denylist.
- /vulnerable/* trusts the token's own `alg` header, the bug behind the
                classic alg=none and RS256->HS256 confusion attacks, and
                never checks the denylist.

The vulnerable code exists for training only.
"""

import base64
import hashlib
import hmac
import json
import time
import uuid

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import Flask, jsonify, request

app = Flask(__name__)

ACCESS_TTL = 900  # 15 minutes
ISSUER = "jwt-lab"

_rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
RSA_PRIVATE_PEM = _rsa_key.private_bytes(
    serialization.Encoding.PEM,
    serialization.PrivateFormat.PKCS8,
    serialization.NoEncryption(),
)
RSA_PUBLIC_PEM = _rsa_key.public_key().public_bytes(
    serialization.Encoding.PEM,
    serialization.PublicFormat.SubjectPublicKeyInfo,
)

USERS = {"qa_user": {"password": "Str0ngP@ss!", "role": "user"}}
REVOKED_JTIS = set()
REFRESH_STORE = {}
CONSUMED_REFRESH = set()


def issue_tokens(username):
    """Issue an RS256 access token plus a rotating refresh token."""
    now = int(time.time())
    access = jwt.encode(
        {
            "sub": username,
            "role": USERS[username]["role"],
            "iss": ISSUER,
            "iat": now,
            "exp": now + ACCESS_TTL,
            "jti": uuid.uuid4().hex,
        },
        RSA_PRIVATE_PEM,
        algorithm="RS256",
    )
    refresh = uuid.uuid4().hex
    REFRESH_STORE[refresh] = username
    return access, refresh


def secure_verify(token):
    """Correct verification: pinned algorithm, full claim check, denylist."""
    claims = jwt.decode(token, RSA_PUBLIC_PEM, algorithms=["RS256"])
    if claims["jti"] in REVOKED_JTIS:
        raise jwt.InvalidTokenError("token revoked")
    return claims


def vulnerable_verify(token):
    """Buggy verification: the token's `alg` header picks the key.

    This mirrors the real-world flaw: an RS256 deployment that selects the
    verification key at runtime ends up using its public key as the HMAC
    secret when a forged token claims HS256 — and skips verification
    entirely when the token claims `none`. It also never consults the
    revocation denylist.
    """
    alg = jwt.get_unverified_header(token).get("alg")
    if alg == "none":
        return jwt.decode(token, options={"verify_signature": False})
    if alg == "HS256":
        # BUG: key selected by the token's alg -> the RS256 public key gets
        # reused as the HMAC secret. PyJWT refuses to do this itself, so a
        # real vulnerable verifier does it by hand — like this one.
        header_b64, payload_b64, sig_b64 = token.split(".")
        claims = json.loads(base64.urlsafe_b64decode(payload_b64 + "=="))
        expected = hmac.new(
            RSA_PUBLIC_PEM, f"{header_b64}.{payload_b64}".encode(), hashlib.sha256
        ).digest()
        if not hmac.compare_digest(
            base64.urlsafe_b64decode(sig_b64 + "=="), expected
        ):
            raise jwt.InvalidTokenError("bad signature")
        if claims.get("exp", 0) < time.time():
            raise jwt.InvalidTokenError("token expired")
        return claims
    return jwt.decode(token, RSA_PUBLIC_PEM, algorithms=["RS256"])


def _profile(verify):
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return jsonify({"error": "missing bearer token"}), 401
    try:
        claims = verify(header.removeprefix("Bearer "))
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid token"}), 401
    return jsonify({"sub": claims["sub"], "role": claims["role"]}), 200


@app.post("/oauth/token")
def token():
    body = request.get_json(silent=True) or {}
    user = USERS.get(body.get("username", ""))
    if not user or user["password"] != body.get("password"):
        return jsonify({"error": "invalid credentials"}), 401
    access, refresh = issue_tokens(body["username"])
    return jsonify(
        {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "Bearer",
            "expires_in": ACCESS_TTL,
        }
    )


@app.post("/oauth/refresh")
def refresh():
    """Rotate the pair: a consumed refresh token dies, and replaying it
    revokes the whole family (RFC 6819 threat model)."""
    body = request.get_json(silent=True) or {}
    old = body.get("refresh_token", "")
    if old in CONSUMED_REFRESH:
        # Replay detected: a stolen token is being reused, so the whole
        # family goes down (RFC 6819 threat model).
        REFRESH_STORE.clear()
        return jsonify({"error": "refresh token family revoked"}), 401
    if old not in REFRESH_STORE:
        return jsonify({"error": "invalid refresh token"}), 401
    username = REFRESH_STORE.pop(old)
    CONSUMED_REFRESH.add(old)
    access, new_refresh = issue_tokens(username)
    return jsonify(
        {
            "access_token": access,
            "refresh_token": new_refresh,
            "token_type": "Bearer",
            "expires_in": ACCESS_TTL,
        }
    )


@app.post("/logout")
def logout():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return jsonify({"error": "missing bearer token"}), 401
    try:
        claims = jwt.decode(
            header.removeprefix("Bearer "), RSA_PUBLIC_PEM, algorithms=["RS256"]
        )
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid token"}), 401
    REVOKED_JTIS.add(claims["jti"])
    return jsonify({"status": "logged out"}), 200


@app.get("/.well-known/jwks.json")
def jwks():
    return jsonify({"note": "RSA public key served via PEM in this lab"}), 200


@app.get("/secure/api/profile")
def secure_profile():
    return _profile(secure_verify)


@app.get("/vulnerable/api/profile")
def vulnerable_profile():
    return _profile(vulnerable_verify)


if __name__ == "__main__":
    app.run(debug=False, port=5000)
