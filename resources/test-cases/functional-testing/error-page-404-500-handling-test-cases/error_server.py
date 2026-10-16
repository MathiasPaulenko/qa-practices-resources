"""Mock error-page server for the error-page test cases.

A single-file http.server that serves the error states the article covers:
custom 404/500/403/413/429/503 pages with correct status codes and headers,
JSON 404 content negotiation, a redirect chain ending at 404, a redirect
loop, and two deliberately misconfigured endpoints (/misconfigured/...) that
reproduce a soft 404 and a stack-trace leak so the negative cases can detect
them.

Run:
    python error_server.py            # serves on http://127.0.0.1:8791
    ERROR_PORT=0 python error_server.py   # any free port, printed to stdout
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import threading

UPLOAD_LIMIT_BYTES = 10 * 1024 * 1024  # 10 MB
RATE_LIMIT_PER_MINUTE = 60

PAGE_404 = """<!doctype html>
<html><head>
<meta name="robots" content="noindex">
<title>Page Not Found — UrbanThreads</title>
</head><body>
<header><a href="/">UrbanThreads</a></header>
<h1>Page Not Found</h1>
<p>The page you are looking for has moved or no longer exists.</p>
<form action="/search" method="get">
  <label for="q">Search</label>
  <input id="q" name="q" type="search" placeholder="Search products">
</form>
<nav>
  <a href="/">Home</a>
  <a href="/shop">Shop</a>
  <a href="/blog">Blog</a>
</nav>
<section class="suggestions">
  <a href="/shop/summer-collection">Summer collection</a>
  <a href="/blog/fit-guide">Fit guide</a>
  <a href="/shop/sale">Sale</a>
</section>
</body></html>"""

PAGE_500 = """<!doctype html>
<html><head>
<meta name="robots" content="noindex">
<title>Something went wrong — UrbanThreads</title>
</head><body>
<h1>Something went wrong</h1>
<p>Our team has been notified. Please try again in a few minutes.</p>
<a href="/">Back to home</a>
<a href="/contact">Contact support</a>
</body></html>"""

PAGE_403 = """<!doctype html>
<html><head><title>Forbidden — UrbanThreads</title></head><body>
<h1>Access denied</h1>
<p>You need to sign in to see this page.</p>
<a href="/login">Log in</a>
</body></html>"""

PAGE_503 = """<!doctype html>
<html><head><title>Maintenance — UrbanThreads</title></head><body>
<h1>We will be right back</h1>
<p>UrbanThreads is down for scheduled maintenance. Expected back at 14:00 UTC.</p>
</body></html>"""

PAGE_LIMIT = """<!doctype html>
<html><head><title>Too many requests — UrbanThreads</title></head><body>
<h1>Slow down</h1>
<p>You have hit the request limit. Wait a moment and try again.</p>
</body></html>"""

STACK_TRACE_LEAK = """<!doctype html>
<html><body>
<h1>Internal Server Error</h1>
<pre>Traceback (most recent call last):
  File "/srv/urbanthreads/app/views.py", line 88, in checkout
    payment.charge(customer_id, db_url="postgres://shop:s3cret@db.internal:5432/shop")
InternalError: connection refused
</pre>
</body></html>"""

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://urbanthreads.com/</loc></url>
  <url><loc>https://urbanthreads.com/shop</loc></url>
  <url><loc>https://urbanthreads.com/blog</loc></url>
</urlset>"""


class ErrorPageHandler(BaseHTTPRequestHandler):
    server_version = "UrbanThreads"  # minimized: no version/OS tokens
    sys_version = ""

    _rate_counter = 0
    _rate_lock = threading.Lock()

    def _send_html(self, status: int, body: str, extra_headers: dict | None = None) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        for k, v in (extra_headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    def _send_json_404(self) -> None:
        body = json.dumps({
            "error": "Not Found",
            "message": "Product 99999 not found",
            "status": 404,
        }).encode("utf-8")
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _redirect(self, location: str) -> None:
        self.send_response(301)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_HEAD(self) -> None:  # noqa: N802 - http.server API
        self.do_GET()

    def do_GET(self) -> None:  # noqa: N802 - http.server API
        path = self.path.split("?")[0]

        if path == "/soft404" or path == "/misconfigured/404":
            # Bug demo: 404 content with status 200 (soft 404).
            self._send_html(200, PAGE_404)
            return
        if path == "/misconfigured/500-debug":
            # Bug demo: stack trace + credentials leaked to the client.
            self._send_html(500, STACK_TRACE_LEAK)
            return
        if path == "/loop":
            self._redirect("/loop")
            return
        if path == "/old-product":
            self._redirect("/product/legacy-summer-sneakers-2024")
            return
        if path == "/sitemap.xml":
            payload = SITEMAP.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/xml")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(payload)
            return
        if path == "/ratelimited" or path.startswith("/api/ratelimited"):
            with self._rate_lock:
                ErrorPageHandler._rate_counter += 1
                count = ErrorPageHandler._rate_counter
            if count > RATE_LIMIT_PER_MINUTE:
                self._send_html(429, PAGE_LIMIT, {
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(RATE_LIMIT_PER_MINUTE),
                    "X-RateLimit-Remaining": "0",
                })
            else:
                self._send_html(200, "<html><body>ok</body></html>")
            return
        if path.startswith("/api/"):
            if "application/json" in self.headers.get("Accept", ""):
                self._send_json_404()
            else:
                self._send_html(404, PAGE_404)
            return
        if path == "/boom" or path == "/checkout/payment":
            self._send_html(500, PAGE_500, {"Cache-Control": "no-store"})
            return
        if path == "/admin/reports":
            self._send_html(403, PAGE_403)
            return
        if path == "/maintenance":
            self._send_html(503, PAGE_503, {"Retry-After": "3600"})
            return
        if path in ("/", "/shop", "/blog"):
            self._send_html(200, "<html><body><h1>UrbanThreads</h1></body></html>")
            return
        # Default: real 404 with the custom page.
        self._send_html(404, PAGE_404)

    def do_POST(self) -> None:  # noqa: N802 - http.server API
        if self.path.startswith("/returns/upload"):
            length = int(self.headers.get("Content-Length", "0"))
            if length > UPLOAD_LIMIT_BYTES:
                # Drain the body so the client isn't reset mid-upload.
                remaining = length
                while remaining > 0:
                    chunk = self.rfile.read(min(65536, remaining))
                    if not chunk:
                        break
                    remaining -= len(chunk)
                self._send_html(413, PAGE_LIMIT)
                return
            body = self.rfile.read(length)
            self._send_html(200, f"<html><body>uploaded {len(body)} bytes</body></html>")
            return
        self._send_html(404, PAGE_404)

    def log_message(self, *args) -> None:  # quiet for tests
        pass


def run(port: int | None = None) -> None:
    port = int(os.environ.get("ERROR_PORT", port if port is not None else 8791))
    server = ThreadingHTTPServer(("127.0.0.1", port), ErrorPageHandler)
    print(f"Error-page mock listening on http://127.0.0.1:{server.server_port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
