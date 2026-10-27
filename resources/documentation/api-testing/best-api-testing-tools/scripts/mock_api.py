"""Small local API fixture for the companion Postman collection.

Run with Python 3.12+: python3 scripts/mock_api.py
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json


class Handler(BaseHTTPRequestHandler):
    """Serve a deterministic health response for local tool evaluation."""

    def do_GET(self) -> None:
        if self.path != "/v1/health":
            self.send_error(404, "Route not found")
            return

        body = json.dumps({"status": "ok"}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8080), Handler)
    print("Mock API listening on http://127.0.0.1:8080 (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping mock API")
    finally:
        server.server_close()
