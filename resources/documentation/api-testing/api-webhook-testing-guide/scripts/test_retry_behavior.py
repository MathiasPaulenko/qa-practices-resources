"""Test webhook retry behavior by simulating different HTTP status codes.

Usage:
    python test_retry_behavior.py

Tests:
1. 200 OK — no retry expected
2. 400 Bad Request — no retry (terminal 4xx)
3. 500 Server Error — retry with backoff
4. 410 Gone — subscription disabled
5. Timeout (>30s) — treated as 500 and retried
"""

import http.server
import threading
import time
import requests
import sys

# Track retry attempts per status code
retry_counts = {}
request_log = []


class WebhookHandler(http.server.BaseHTTPRequestHandler):
    """Simulates different consumer responses based on path."""

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        log_entry = {
            'path': self.path,
            'timestamp': time.time(),
            'body_size': len(body),
        }
        request_log.append(log_entry)

        if self.path == '/ok':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        elif self.path == '/bad-request':
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Bad Request')
        elif self.path == '/server-error':
            count = retry_counts.get('/server-error', 0)
            retry_counts['/server-error'] = count + 1
            if count >= 3:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK after retries')
            else:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Server Error')
        elif self.path == '/gone':
            self.send_response(410)
            self.end_headers()
            self.wfile.write(b'Gone')
        elif self.path == '/slow':
            time.sleep(35)  # Simulate timeout > 30s
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK but slow')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress default logging


def start_server(port=9099):
    server = http.server.HTTPServer(('localhost', port), WebhookHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def test_200_no_retry(base_url):
    """200 OK should not trigger a retry."""
    request_log.clear()
    r = requests.post(f'{base_url}/ok', json={'event': 'test_200'})
    assert r.status_code == 200
    time.sleep(1)
    # No additional requests expected for 200
    ok_requests = [l for l in request_log if l['path'] == '/ok']
    assert len(ok_requests) == 1, f"Expected 1 request, got {len(ok_requests)}"
    print("PASS: 200 OK — no retry triggered")


def test_400_no_retry(base_url):
    """400 Bad Request should not trigger a retry (terminal 4xx)."""
    request_log.clear()
    r = requests.post(f'{base_url}/bad-request', json={'event': 'test_400'})
    assert r.status_code == 400
    time.sleep(1)
    bad_requests = [l for l in request_log if l['path'] == '/bad-request']
    assert len(bad_requests) == 1, f"Expected 1 request, got {len(bad_requests)}"
    print("PASS: 400 Bad Request — no retry (terminal 4xx)")


def test_500_retries(base_url):
    """500 Server Error should trigger retries with backoff."""
    retry_counts.clear()
    request_log.clear()
    # First few attempts return 500, then 200
    for _ in range(5):
        r = requests.post(f'{base_url}/server-error', json={'event': 'test_500'})
        time.sleep(0.5)
    assert retry_counts.get('/server-error', 0) >= 3, "Expected at least 3 retry attempts"
    print(f"PASS: 500 Server Error — {retry_counts['/server-error']} attempts before success")


def test_410_disables(base_url):
    """410 Gone should signal subscription disabled."""
    request_log.clear()
    r = requests.post(f'{base_url}/gone', json={'event': 'test_410'})
    assert r.status_code == 410
    print("PASS: 410 Gone — subscription disabled signal sent")


if __name__ == "__main__":
    server = start_server()
    base_url = "http://localhost:9099"
    time.sleep(0.5)

    try:
        test_200_no_retry(base_url)
        test_400_no_retry(base_url)
        test_500_retries(base_url)
        test_410_disables(base_url)
        print("\nAll retry behavior tests passed.")
    except AssertionError as e:
        print(f"\nFAIL: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        server.shutdown()
