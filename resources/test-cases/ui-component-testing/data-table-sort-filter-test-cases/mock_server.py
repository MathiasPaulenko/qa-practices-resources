"""Stdlib mock of the fictional DataGrid Pro orders API.

Implements GET /v1/orders with the query contract used in the article:
sort, direction, page, pageSize, status, from, to and search.
Requires a Bearer token in the Authorization header (any non-empty value).
"""

import json
import threading
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

CUSTOMERS = [
    "Acme Corp", "Beta LLC", "Gamma Inc", "Delta Co", "Epsilon Ltd",
    "Zeta SA", "Acme Subsidiary", "Orion Labs", "Nova Systems", "Atlas Group",
]
STATUSES = ["pending", "shipped", "delivered"]
AMOUNTS = [2.50, 10.00, 99.99, 3200.00, 12500.00, 15000.00, 7500.00, 42.00]


def _build_orders():
    orders = []
    base = date(2026, 7, 1)
    for i in range(60):
        orders.append({
            "id": "ORD-%04d" % (5001 + i),
            "customerName": CUSTOMERS[i % len(CUSTOMERS)],
            "amount": round(AMOUNTS[i % len(AMOUNTS)] * (1 + (i % 7) * 0.1), 2),
            "status": STATUSES[i % len(STATUSES)],
            "orderDate": date.fromordinal(base.toordinal() + (i % 45)).isoformat(),
        })
    return orders


ORDERS = _build_orders()


def reset_store():
    """No-op: the dataset is static and read-only."""
    return None


def _sort_key(field):
    def key(order):
        value = order[field]
        if isinstance(value, (int, float)):
            return (0, value)
        return (1, value)
    return key


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/v1/orders":
            self._send(404, {"error": "not_found"})
            return
        if not self.headers.get("Authorization", "").startswith("Bearer "):
            self._send(401, {"error": "unauthorized"})
            return

        params = parse_qs(parsed.query)
        rows = list(ORDERS)

        status = params.get("status", [None])[0]
        if status:
            rows = [r for r in rows if r["status"] == status]

        date_from = params.get("from", [None])[0]
        date_to = params.get("to", [None])[0]
        if date_from:
            rows = [r for r in rows if r["orderDate"] >= date_from]
        if date_to:
            rows = [r for r in rows if r["orderDate"] <= date_to]

        search = params.get("search", [None])[0]
        if search:
            needle = search.lower()
            rows = [
                r for r in rows
                if needle in r["customerName"].lower()
                or needle in r["id"].lower()
                or needle in r["status"].lower()
            ]

        sort_field = params.get("sort", [None])[0]
        if sort_field:
            if sort_field not in ("amount", "orderDate", "customerName", "status", "id"):
                self._send(400, {"error": "invalid_sort_field", "field": sort_field})
                return
            reverse = params.get("direction", ["asc"])[0] == "desc"
            rows.sort(key=_sort_key(sort_field), reverse=reverse)

        try:
            page = max(int(params.get("page", ["1"])[0]), 1)
            page_size = max(int(params.get("pageSize", ["20"])[0]), 1)
        except ValueError:
            self._send(400, {"error": "invalid_pagination"})
            return

        total = len(rows)
        total_pages = max(-(-total // page_size), 1)
        start = (page - 1) * page_size
        page_rows = rows[start:start + page_size]

        payload = {
            "orders": page_rows,
            "page": page,
            "pageSize": page_size,
            "totalItems": total,
            "totalPages": total_pages,
        }
        if sort_field:
            payload["sort"] = {
                "field": sort_field,
                "direction": "desc" if reverse else "asc",
            }
        filters = {}
        if status:
            filters["status"] = status
        if date_from:
            filters["from"] = date_from
        if date_to:
            filters["to"] = date_to
        if filters:
            payload["filters"] = filters
        if search:
            payload["search"] = search

        self._send(200, payload)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = 8080
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("mock on http://127.0.0.1:%d/v1/orders" % port)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    threading.Event().wait()
