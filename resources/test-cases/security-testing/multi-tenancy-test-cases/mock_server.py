"""Stdlib-only multi-tenant mock API for the multi-tenancy test cases.

Two tenants (acme, globex) share one app instance. Tenant context is resolved
from the `X-Tenant-ID` header or from a `tenant` claim embedded in a fake
base64 JWT (`Bearer <b64(payload)>.sig`). All data access is tenant-scoped —
RLS-style — so the suite can exercise real isolation boundaries.

Intentional behaviors to test:
- `GET /api/orders/{id}` returns 403/404 (uniform) for cross-tenant IDs.
- Requests without tenant context get 400/401.
- A shared cache exposes `user:42` without namespace (a leak to detect).
- `DELETE` without the tenant scope never happens: suspension invalidates sessions.

Run standalone: python mock_server.py 8571
"""

import base64
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

TENANTS = {"acme", "globex", "oldco"}
SUSPENDED = {"oldco"}  # suspended tenant — lifecycle edge case

DATA = {
    "acme": {
        "users": {"u-42": {"id": "u-42", "name": "Ana Acme"}},
        "orders": {"A-order-7781": {"id": "A-order-7781", "total": 1200}},
    },
    "globex": {
        "users": {"u-77": {"id": "u-77", "name": "Gus Globex"}},
        "orders": {"B-order-2210": {"id": "B-order-2210", "total": 900}},
    },
    "oldco": {
        "users": {"u-9": {"id": "u-9", "name": "Olaf Oldco"}},
        "orders": {},
    },
}

# A shared "cache" — one key is unnamespaced on purpose (the leak to find).
CACHE = {"acme:user:42": "Ana Acme", "user:42": "LEAKED-CACHE-ENTRY"}


def fake_jwt(tenant: str, sub: str = "u-1") -> str:
    """Build a fake bearer token: base64(payload).sig — only for tests."""
    payload = base64.urlsafe_b64encode(
        json.dumps({"sub": sub, "tenant": tenant}).encode()
    ).decode()
    return f"{payload}.sig"


def decode_tenant(auth_header: str) -> str | None:
    """Extract the tenant claim; returns None on malformed tokens."""
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header[7:]
    parts = token.split(".")
    if len(parts) != 2:
        return None  # malformed token shape
    try:
        payload = json.loads(base64.urlsafe_b64decode(parts[0] + "=="))
        return payload.get("tenant")
    except Exception:
        return None


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: dict):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _tenant(self) -> tuple[str | None, int | None]:
        """Resolve tenant from header or token. Returns (tenant, error_code)."""
        header = self.headers.get("X-Tenant-ID")
        token_tenant = decode_tenant(self.headers.get("Authorization", ""))
        tenant = header or token_tenant
        if tenant is None:
            return None, 401
        if tenant not in TENANTS:
            return None, 403
        if tenant in SUSPENDED:
            return None, 403
        if header and token_tenant and header != token_tenant:
            return None, 403  # header/claim mismatch
        return tenant, None

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/health":
            self._send(200, {"status": "ok", "tenants": sorted(TENANTS)})
            return

        tenant, err = self._tenant()
        if err:
            self._send(err, {"error": "unauthorized" if err == 401 else "forbidden"})
            return

        if path == "/api/me":
            user = next(iter(DATA[tenant]["users"].values()))
            self._send(200, {"tenant": tenant, "user": user})
            return

        if path.startswith("/api/orders/"):
            oid = path.rsplit("/", 1)[-1]
            order = DATA[tenant]["orders"].get(oid)
            if order is None:
                # uniform 403 for cross-tenant or unknown IDs — no enumeration
                self._send(403, {"error": "forbidden"})
            else:
                self._send(200, order)
            return

        if path == "/api/cache/keys":
            # leaks the shared cache namespace — the unnamespaced key shows up
            self._send(200, {"keys": sorted(CACHE)})
            return

        self._send(404, {"error": "unknown endpoint"})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8571
    print(f"mock on :{port} — tenants {sorted(TENANTS)}")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
