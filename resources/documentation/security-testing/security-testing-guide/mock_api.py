"""Minimal HTTP API fixture for the BOLA test suite.

Two users (alice, bob) each own orders. `GET /api/v1/orders/{id}` returns the
order only when the Bearer token belongs to its owner — that is the access
control rule the tests verify. Stdlib only, no dependencies.
"""

import json
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

USERS = {
    "alice@medisync.test": {"password": "ValidPass123!", "id": "u-alice"},
    "bob@medisync.test": {"password": "OtherPass123!", "id": "u-bob"},
}

# order_id -> owner user id
ORDERS = {
    "42": {"owner": "u-alice", "item": "Prescription refill", "total": 19.99},
    "77": {"owner": "u-bob", "item": "Lab test", "total": 59.0},
}

_TOKENS = {}  # token -> user id


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _bearer_user(self) -> str | None:
        header = self.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return None
        return _TOKENS.get(header.removeprefix("Bearer ").strip())

    def log_message(self, *_args) -> None:  # keep pytest output clean
        pass

    def do_POST(self) -> None:
        if self.path != "/api/v1/token":
            return self._json(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length", 0))
        creds = json.loads(self.rfile.read(length) or b"{}")
        user = USERS.get(creds.get("email", ""))
        if not user or user["password"] != creds.get("password"):
            return self._json(401, {"error": "invalid credentials"})
        token = secrets.token_urlsafe(24)
        _TOKENS[token] = user["id"]
        self._json(200, {"access_token": token, "token_type": "bearer"})

    def do_GET(self) -> None:
        if not self.path.startswith("/api/v1/orders/"):
            return self._json(404, {"error": "not found"})
        order_id = self.path.rsplit("/", 1)[-1]
        order = ORDERS.get(order_id)
        user_id = self._bearer_user()
        if user_id is None:
            return self._json(401, {"error": "missing or invalid token"})
        if order is None:
            return self._json(404, {"error": "order not found"})
        if order["owner"] != user_id:
            return self._json(403, {"error": "forbidden"})
        self._json(200, {"id": order_id, **order})


def make_server(port: int = 0) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    server = make_server(8080)
    print(f"Mock API on http://127.0.0.1:{server.server_port}/api/v1")
    server.serve_forever()
