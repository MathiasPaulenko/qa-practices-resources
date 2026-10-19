"""Stdlib mock of the fictional RangeSlider Pro API.

Implements the endpoints used in the article's curl examples:
  GET  /v1/products?minPrice&maxPrice&step&page&pageSize   (Bearer auth)
  POST /v1/sliders/validate                               (min/max/step/value)
  POST /v1/sliders/validate-range                         (left/right/gap)
  POST /v1/users/{userId}/preferences                     (Bearer auth)

Run standalone:  python mock_server.py  ->  http://127.0.0.1:8080
"""

import json
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

SECTORS = ["Technology", "Energy", "Healthcare", "Finance", "Consumer"]
NAMES = ["TechCorp", "EnergyCo", "BioHealth", "FinGroup", "RetailStar",
         "AeroDyne", "MediCore", "BankWise", "CloudNine", "GreenGrid"]


def _build_products():
    products = []
    for i in range(342):
        price = 5.0 + (i % 200) * 5.0  # 5.00 .. 1000.00 in $5 steps
        products.append({
            "id": "PRD-%03d" % (i + 1),
            "name": "%s Stock" % NAMES[i % len(NAMES)],
            "price": round(price, 2),
            "sector": SECTORS[i % len(SECTORS)],
        })
    return products


PRODUCTS = _build_products()
PREFERENCES = {}


def reset_store():
    """Clear saved preferences between tests."""
    PREFERENCES.clear()


def _authed(handler):
    auth = handler.headers.get("Authorization", "")
    return auth.startswith("Bearer ") and len(auth) > 7


def _snap(value, min_v, max_v, step):
    """Clamp to range and round to the nearest step like the slider widget."""
    value = max(min_v, min(max_v, value))
    steps = round((value - min_v) / step)
    return round(min_v + steps * step, 10)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode())
        except (ValueError, UnicodeDecodeError):
            return None

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/v1/products":
            self._send(404, {"error": "Not found"})
            return
        if not _authed(self):
            self._send(401, {"error": "Missing or invalid bearer token"})
            return

        qs = parse_qs(parsed.query)
        min_price = float(qs.get("minPrice", ["0"])[0])
        max_price = float(qs.get("maxPrice", ["1000"])[0])
        step = float(qs.get("step", ["5"])[0])
        page = int(qs.get("page", ["1"])[0])
        page_size = int(qs.get("pageSize", ["20"])[0])

        filtered = [p for p in PRODUCTS if min_price <= p["price"] <= max_price]
        start = (page - 1) * page_size
        self._send(200, {
            "products": filtered[start:start + page_size],
            "page": page,
            "pageSize": page_size,
            "totalItems": len(filtered),
            "filter": {"minPrice": min_price, "maxPrice": max_price, "step": step},
        })

    def do_POST(self):
        parsed = urlparse(self.path)
        body = self._json_body()
        if body is None:
            self._send(400, {"error": "Invalid JSON body"})
            return

        if parsed.path == "/v1/sliders/validate":
            self._validate(body)
        elif parsed.path == "/v1/sliders/validate-range":
            self._validate_range(body)
        elif re.fullmatch(r"/v1/users/[\w-]+/preferences", parsed.path):
            self._save_preference(parsed.path.split("/")[3], body)
        else:
            self._send(404, {"error": "Not found"})

    def _validate(self, body):
        min_v = body.get("min", 0)
        max_v = body.get("max", 1000)
        step = body.get("step", 5)
        value = body.get("value")

        if value is None or not isinstance(value, (int, float)):
            self._send(400, {"error": "value must be a number"})
            return

        snapped = _snap(value, min_v, max_v, step)
        if value < min_v or value > max_v:
            self._send(200, {
                "valid": False,
                "value": value, "min": min_v, "max": max_v, "step": step,
                "error": "Value %s is outside the range %s-%s" % (value, min_v, max_v),
                "nearestValidValue": snapped,
            })
        elif abs(value - snapped) > 1e-9:
            self._send(200, {
                "valid": False,
                "value": value, "min": min_v, "max": max_v, "step": step,
                "error": "Value %s is not a multiple of step %s" % (value, step),
                "nearestValidValue": snapped,
            })
        else:
            self._send(200, {
                "valid": True,
                "value": value, "min": min_v, "max": max_v, "step": step,
            })

    def _validate_range(self, body):
        left = body.get("leftHandle")
        right = body.get("rightHandle")
        gap = body.get("gap", body.get("minGap", 0))

        if left is None or right is None:
            self._send(400, {"error": "leftHandle and rightHandle are required"})
            return
        if left >= right:
            self._send(200, {
                "valid": False,
                "error": "Left handle (%s) must be less than right handle (%s)" % (left, right),
                "leftHandle": left,
                "rightHandle": right,
                "minGap": gap,
            })
        elif right - left < gap:
            self._send(200, {
                "valid": False,
                "error": "Range %s is smaller than minGap %s" % (right - left, gap),
                "leftHandle": left,
                "rightHandle": right,
                "minGap": gap,
            })
        else:
            self._send(200, {
                "valid": True,
                "leftHandle": left,
                "rightHandle": right,
                "minGap": gap,
            })

    def _save_preference(self, user_id, body):
        if not _authed(self):
            self._send(401, {"error": "Missing or invalid bearer token"})
            return
        required = {"filterName", "minPrice", "maxPrice", "step"}
        if not required.issubset(body):
            self._send(400, {"error": "Missing fields: %s" % sorted(required - set(body))})
            return
        pref_id = "PREF-%03d" % (101 + len(PREFERENCES))
        PREFERENCES[pref_id] = dict(body, userId=user_id)
        self._send(200, dict(
            {"preferenceId": pref_id, "userId": user_id},
            **{k: body[k] for k in ("filterName", "minPrice", "maxPrice", "step")},
            savedAt="2026-10-19T10:00:00Z",
        ))

    def log_message(self, *args):
        pass


def start_server(port=8080):
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


if __name__ == "__main__":
    start_server(8080)
    print("Mock listening on http://127.0.0.1:8080  (Ctrl+C to stop)")
    threading.Event().wait()
