"""pytest suite for the TaskFlow-style API key lab.

Each test maps to a TC from the resource: creation, masking, scope
enforcement, revocation latency, rotation grace, deletion, expiry,
rate limiting, IP allowlists and audit-log hygiene.

Run with: pytest -v
"""

import re
import time

import pytest

import app as lab


@pytest.fixture()
def client():
    lab.KEYS.clear()
    lab.AUDIT_LOG.clear()
    lab.REQUEST_COUNTS.clear()
    lab.GRACE_SECONDS = 24 * 3600
    lab.RATE_LIMIT = 1000
    lab.app.config["TESTING"] = True
    with lab.app.test_client() as c:
        yield c


def create(client, **overrides):
    body = {
        "name": "Production dashboard key",
        "environment": "live",
        "scopes": ["tasks:read", "projects:read"],
    }
    body.update(overrides)
    resp = client.post(
        "/v1/api-keys",
        json=body,
        headers={"Authorization": f"Bearer {lab.ADMIN_TOKEN}"},
    )
    assert resp.status_code == 201
    return resp.get_json()


def auth(raw):
    return {"Authorization": f"Bearer {raw}"}


def test_create_returns_full_key_once(client):
    """TC001 — creation returns the full tf_live_ key exactly once."""
    rec = create(client)
    assert rec["key"].startswith("tf_live_")
    assert len(rec["key"]) > 30
    assert rec["scopes"] == ["tasks:read", "projects:read"]
    assert rec["id"].startswith("ak_")

    again = client.get(
        f"/v1/api-keys/{rec['id']}",
        headers={"Authorization": f"Bearer {lab.ADMIN_TOKEN}"},
    ).get_json()
    assert "*" in again["key"]
    assert rec["key"] not in again["key"]


def test_list_never_returns_raw_secret(client):
    """TC002 — the list endpoint exposes masked values only."""
    rec = create(client)
    listing = client.get(
        "/v1/api-keys",
        headers={"Authorization": f"Bearer {lab.ADMIN_TOKEN}"},
    ).get_json()
    assert listing["data"][0]["key"] == rec["key"][:8] + "*" * 36 + rec["key"][-4:]
    assert rec["key"] not in str(listing)


def test_valid_key_authenticates(client):
    """TC005 — a live key with tasks:read reads tasks."""
    rec = create(client)
    resp = client.get("/v1/tasks", headers=auth(rec["key"]))
    assert resp.status_code == 200
    assert resp.get_json()["data"][0]["id"] == "task_1"


def test_scope_enforcement_blocks_writes(client):
    """TC006 — a read-only key is refused on write endpoints."""
    rec = create(client)
    assert client.get("/v1/tasks", headers=auth(rec["key"])).status_code == 200
    denied = client.post("/v1/tasks", json={"title": "x"}, headers=auth(rec["key"]))
    assert denied.status_code == 403
    assert denied.get_json()["error"] == "forbidden"


def test_revoked_key_fails_immediately(client):
    """TC007 — revocation propagates with no caching delay."""
    rec = create(client)
    assert client.get("/v1/tasks", headers=auth(rec["key"])).status_code == 200
    client.post(
        f"/v1/api-keys/{rec['id']}/revoke",
        headers={"Authorization": f"Bearer {lab.ADMIN_TOKEN}"},
    )
    assert client.get("/v1/tasks", headers=auth(rec["key"])).status_code == 401


def test_deleted_key_is_gone(client):
    """TC008 — DELETE removes the record and kills the credential."""
    rec = create(client)
    resp = client.delete(
        f"/v1/api-keys/{rec['id']}",
        headers={"Authorization": f"Bearer {lab.ADMIN_TOKEN}"},
    )
    assert resp.status_code == 204
    assert rec["id"] not in lab.KEYS
    assert client.get("/v1/tasks", headers=auth(rec["key"])).status_code == 401


def test_expired_key_rejected(client):
    """TC009 — a key past expires_at returns 401."""
    rec = create(client, expires_at=time.time() - 1)
    resp = client.get("/v1/tasks", headers=auth(rec["key"]))
    assert resp.status_code == 401
    assert "expired" in resp.get_json()["error"]


def test_rotation_grace_period(client):
    """TC010 — the old key works during grace, then dies."""
    lab.GRACE_SECONDS = 0.2
    old = create(client)
    rotated = client.post(
        f"/v1/api-keys/{old['id']}/rotate",
        headers={"Authorization": f"Bearer {lab.ADMIN_TOKEN}"},
    )
    assert rotated.status_code == 201
    new = rotated.get_json()
    assert new["id"] != old["id"]

    # new key works immediately; old still inside the grace window
    assert client.get("/v1/tasks", headers=auth(new["key"])).status_code == 200
    assert client.get("/v1/tasks", headers=auth(old["key"])).status_code == 200

    time.sleep(0.25)
    assert client.get("/v1/tasks", headers=auth(old["key"])).status_code == 401


def test_rate_limit_returns_429_with_retry_after(client):
    """TC011 — the request past the limit gets 429 + Retry-After."""
    lab.RATE_LIMIT = 5
    rec = create(client)
    for _ in range(5):
        assert client.get("/v1/tasks", headers=auth(rec["key"])).status_code == 200
    resp = client.get("/v1/tasks", headers=auth(rec["key"]))
    assert resp.status_code == 429
    assert resp.headers["Retry-After"]
    assert resp.headers["X-RateLimit-Remaining"] == "0"


def test_ip_allowlist_blocks_unknown_source(client):
    """TC012 — a restricted key only answers from the allowed IP."""
    rec = create(client, ip_allowlist=["203.0.113.10"])
    resp = client.get("/v1/tasks", headers=auth(rec["key"]))
    assert resp.status_code == 403  # test client remote_addr is 127.0.0.1


def test_key_in_query_string_rejected(client):
    """Edge case — credentials in the URL get 400, not auth."""
    rec = create(client)
    resp = client.get(f"/v1/tasks?api_key={rec['key']}")
    assert resp.status_code == 400


def test_audit_log_has_events_without_secrets(client):
    """TC013 — lifecycle events logged with actor; raw key never appears."""
    rec = create(client)
    client.get("/v1/tasks", headers=auth(rec["key"]))
    client.post(
        f"/v1/api-keys/{rec['id']}/revoke",
        headers={"Authorization": f"Bearer {lab.ADMIN_TOKEN}"},
    )
    log = client.get(
        "/v1/audit-log",
        headers={"Authorization": f"Bearer {lab.ADMIN_TOKEN}"},
    ).get_json()["data"]
    actions = [e["action"] for e in log if e["key_id"] == rec["id"]]
    assert actions == ["create", "use", "revoke"]
    assert all(e["actor"] == "admin@taskflow.io" for e in log)
    assert rec["key"] not in str(log)


def test_generated_keys_have_entropy_and_no_collisions(client):
    """ES/edge — 100 keys, unique, urlsafe alphabet, >=32-char secret part."""
    seen = set()
    for _ in range(100):
        rec = create(client)
        seen.add(rec["key"])
        secret_part = rec["key"].split("_", 2)[2]
        assert len(secret_part) >= 32
        assert re.fullmatch(r"[A-Za-z0-9_-]+", secret_part)
    assert len(seen) == 100
