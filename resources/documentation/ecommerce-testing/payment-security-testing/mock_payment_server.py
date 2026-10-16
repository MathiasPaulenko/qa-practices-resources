"""Stdlib mock payment API + webhook receiver for the payment security testing guide.

Two endpoints, both deliberately strict so the pytest suite can probe them:

- POST /api/checkout/pay — recomputes the order total server-side and
  deduplicates on the Idempotency-Key header.
- POST /webhooks/payments — verifies a Stripe-style HMAC signature
  (t=timestamp,v1=hex) with a 300-second tolerance window.
"""

import hashlib
import hmac
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

WEBHOOK_SECRET = b"whsec_test_4f8d2c9e1b7a"
TOLERANCE_SECONDS = 300

ORDERS = {
    "ord_7f3a9c": {"amount": 99.99, "currency": "USD"},
    "ord_bad": {"amount": 12.50, "currency": "EUR"},
}

# Shared state — tests read these to assert behavior.
charges = []  # created charges: {"id": ..., "amount": ..., "currency": ...}
idempotency_index = {}  # Idempotency-Key -> response body
webhook_events = []  # accepted webhook payloads


def sign_webhook(payload: bytes, timestamp: int | None = None, secret: bytes = WEBHOOK_SECRET) -> str:
    """Build a valid signature header value; the tests also use it to craft attacks."""
    ts = timestamp if timestamp is not None else int(time.time())
    signed = f"{ts}.".encode() + payload
    digest = hmac.new(secret, signed, hashlib.sha256).hexdigest()
    return f"t={ts},v1={digest}"


class PaymentHandler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler contract
        if self.path == "/api/checkout/pay":
            self._handle_pay()
        elif self.path == "/webhooks/payments":
            self._handle_webhook()
        else:
            self._send(404, {"error": "not found"})

    def _handle_pay(self) -> None:
        body = self._read_json()
        order = ORDERS.get(body.get("orderId"))
        if order is None:
            self._send(404, {"error": "unknown order"})
            return
        # Server-side recompute: the client's amount/currency are never trusted.
        if body.get("amount") != order["amount"] or body.get("currency") != order["currency"]:
            self._send(400, {"error": "amount mismatch"})
            return
        key = self.headers.get("Idempotency-Key")
        if key and key in idempotency_index:
            self._send(200, idempotency_index[key])
            return
        charge = {
            "id": f"ch_{len(charges) + 1:04d}",
            "amount": order["amount"],
            "currency": order["currency"],
            "status": "succeeded",
        }
        charges.append(charge)
        if key:
            idempotency_index[key] = charge
        self._send(200, charge)

    def _handle_webhook(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        payload = self.rfile.read(length)
        header = self.headers.get("X-Payment-Signature", "")
        try:
            parts = dict(kv.split("=", 1) for kv in header.split(","))
            signed = f"{parts['t']}.".encode() + payload
            expected = hmac.new(WEBHOOK_SECRET, signed, hashlib.sha256).hexdigest()
            valid_sig = hmac.compare_digest(expected, parts["v1"])
            fresh = abs(time.time() - int(parts["t"])) <= TOLERANCE_SECONDS
        except (KeyError, ValueError):
            valid_sig = fresh = False
        if not (valid_sig and fresh):
            self._send(401, {"error": "invalid signature"})
            return
        event = json.loads(payload or b"{}")
        webhook_events.append(event)
        self._send(200, {"received": True})

    def log_message(self, *_args) -> None:  # keep test output clean
        pass


def start_server(port: int = 0) -> tuple[ThreadingHTTPServer, int, threading.Thread]:
    """Start the mock server on an ephemeral port; returns (server, port, thread)."""
    server = ThreadingHTTPServer(("127.0.0.1", port), PaymentHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, server.server_address[1], thread


if __name__ == "__main__":
    srv, port, _thread = start_server(8765)
    print(f"Mock payment server on http://127.0.0.1:{port} (Ctrl+C to stop)")
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        srv.shutdown()
