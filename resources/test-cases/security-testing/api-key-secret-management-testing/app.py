"""API key lab for the API Key & Secret Management Testing resource.

A minimal Flask app that mimics the TaskFlow key lifecycle:

- POST   /v1/api-keys              create a key (full value returned once)
- GET    /v1/api-keys              list keys, masked values only
- GET    /v1/api-keys/<key_id>     single key, masked value only
- POST   /v1/api-keys/<key_id>/revoke   instant revocation
- POST   /v1/api-keys/<key_id>/rotate   issue a new key, keep the old one
                                       alive for GRACE_SECONDS
- DELETE /v1/api-keys/<key_id>     remove the record entirely
- GET    /v1/tasks                 Bearer auth + scope + rate limit + IP list
- GET    /v1/audit-log             lifecycle events, never the secret

Only key hashes are stored. The audit log records key ids, never values.
"""

import hashlib
import secrets
import time
import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)

ADMIN_TOKEN = "test-admin-token"
GRACE_SECONDS = 24 * 3600
RATE_LIMIT = 1000          # requests per window
RATE_WINDOW = 60           # seconds

# key_id -> record dict. The raw secret is never stored: hash + mask only.
KEYS = {}
AUDIT_LOG = []
REQUEST_COUNTS = {}        # key_id -> [timestamps]


def _hash(raw):
    return hashlib.sha256(raw.encode()).hexdigest()


def _mask(raw):
    return raw[:8] + "*" * 36 + raw[-4:]


def _log(action, key_id, detail=""):
    AUDIT_LOG.append({
        "action": action,
        "key_id": key_id,
        "actor": "admin@taskflow.io",
        "timestamp": int(time.time()),
        "ip_address": request.remote_addr,
        "endpoint": request.path,
        "detail": detail,
    })


def _admin_ok():
    return request.headers.get("Authorization") == f"Bearer {ADMIN_TOKEN}"


def _find_key(raw):
    digest = _hash(raw)
    for key_id, rec in KEYS.items():
        if rec["hash"] == digest:
            return key_id, rec
    return None, None


def _rate_ok(key_id):
    now = time.time()
    hits = [t for t in REQUEST_COUNTS.get(key_id, []) if now - t < RATE_WINDOW]
    REQUEST_COUNTS[key_id] = hits
    if len(hits) >= RATE_LIMIT:
        return False
    hits.append(now)
    return True


def _public(rec):
    return {
        "id": rec["id"],
        "name": rec["name"],
        "environment": rec["environment"],
        "prefix": rec["prefix"],
        "scopes": rec["scopes"],
        "key": rec["masked"],
        "created_at": rec["created_at"],
        "expires_at": rec["expires_at"],
        "revoked": rec["revoked"],
    }


@app.post("/v1/api-keys")
def create_key():
    if not _admin_ok():
        return jsonify({"error": "unauthorized"}), 401
    body = request.get_json(silent=True) or {}
    raw = "tf_" + ("test_" if body.get("environment") == "test" else "live_") \
        + secrets.token_urlsafe(32)
    rec = {
        "id": "ak_" + uuid.uuid4().hex[:16],
        "name": body.get("name", "unnamed"),
        "environment": body.get("environment", "live"),
        "prefix": raw[:7],
        "scopes": list(body.get("scopes", [])),
        "hash": _hash(raw),
        "masked": _mask(raw),
        "created_at": int(time.time()),
        "expires_at": body.get("expires_at"),
        "grace_until": None,
        "revoked": False,
        "ip_allowlist": body.get("ip_allowlist"),
    }
    KEYS[rec["id"]] = rec
    _log("create", rec["id"])
    out = _public(rec)
    out["key"] = raw  # full value is returned exactly once
    return jsonify(out), 201


@app.get("/v1/api-keys")
def list_keys():
    if not _admin_ok():
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"data": [_public(r) for r in KEYS.values()]})


@app.get("/v1/api-keys/<key_id>")
def read_key(key_id):
    if not _admin_ok():
        return jsonify({"error": "unauthorized"}), 401
    rec = KEYS.get(key_id)
    if not rec:
        return jsonify({"error": "not found"}), 404
    return jsonify(_public(rec))


@app.post("/v1/api-keys/<key_id>/revoke")
def revoke_key(key_id):
    if not _admin_ok():
        return jsonify({"error": "unauthorized"}), 401
    rec = KEYS.get(key_id)
    if not rec:
        return jsonify({"error": "not found"}), 404
    rec["revoked"] = True
    rec["grace_until"] = None
    _log("revoke", key_id)
    return jsonify({"id": key_id, "revoked": True})


@app.post("/v1/api-keys/<key_id>/rotate")
def rotate_key(key_id):
    if not _admin_ok():
        return jsonify({"error": "unauthorized"}), 401
    old = KEYS.get(key_id)
    if not old:
        return jsonify({"error": "not found"}), 404
    raw = old["prefix"] + secrets.token_urlsafe(32)
    rec = dict(old)
    rec.update({
        "id": "ak_" + uuid.uuid4().hex[:16],
        "hash": _hash(raw),
        "masked": _mask(raw),
        "created_at": int(time.time()),
        "revoked": False,
        "grace_until": None,
    })
    KEYS[rec["id"]] = rec
    old["grace_until"] = time.time() + GRACE_SECONDS
    _log("rotate", key_id, detail=f"successor={rec['id']}")
    out = _public(rec)
    out["key"] = raw
    return jsonify(out), 201


@app.delete("/v1/api-keys/<key_id>")
def delete_key(key_id):
    if not _admin_ok():
        return jsonify({"error": "unauthorized"}), 401
    if key_id not in KEYS:
        return jsonify({"error": "not found"}), 404
    del KEYS[key_id]
    _log("delete", key_id)
    return "", 204


@app.route("/v1/tasks", methods=["GET", "POST"])
def tasks():
    if "api_key=" in request.query_string.decode():
        _log("use", "unknown", detail="key in query string")
        return jsonify({"error": "credentials belong in headers"}), 400
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "missing bearer token"}), 401
    key_id, rec = _find_key(auth[7:])
    now = time.time()
    if not rec:
        return jsonify({"error": "invalid key"}), 401
    if rec["revoked"]:
        return jsonify({"error": "key revoked"}), 401
    if rec["expires_at"] and now > float(rec["expires_at"]):
        return jsonify({"error": "key expired"}), 401
    if rec["grace_until"] and now < rec["grace_until"]:
        pass  # old key still valid during the rotation grace window
    elif rec["grace_until"] and now >= rec["grace_until"]:
        return jsonify({"error": "key rotated out"}), 401
    if rec["ip_allowlist"] and request.remote_addr not in rec["ip_allowlist"]:
        return jsonify({"error": "forbidden"}), 403
    needed = "tasks:read" if request.method == "GET" else "tasks:write"
    if needed not in rec["scopes"]:
        _log("use", key_id, detail=f"scope_denied:{needed}")
        return jsonify({"error": "forbidden"}), 403
    if not _rate_ok(key_id):
        resp = jsonify({"error": "rate limit exceeded"})
        resp.status_code = 429
        resp.headers["Retry-After"] = str(RATE_WINDOW)
        resp.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
        resp.headers["X-RateLimit-Remaining"] = "0"
        return resp
    _log("use", key_id)
    if request.method == "POST":
        body = request.get_json(silent=True) or {}
        return jsonify({"id": "task_new", "title": body.get("title", ""), "status": "open"}), 201
    return jsonify({"data": [{"id": "task_1", "title": "Draft Q3 roadmap", "status": "open"}]})


@app.get("/v1/audit-log")
def audit_log():
    if not _admin_ok():
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"data": AUDIT_LOG})


if __name__ == "__main__":
    app.run(port=5055)
