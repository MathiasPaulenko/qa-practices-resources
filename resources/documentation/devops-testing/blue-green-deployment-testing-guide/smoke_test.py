"""Post-switch smoke test: verify the core user journeys still work on green.

Hits a small set of endpoints after the cutover and fails fast on any
non-2xx response. Intended to run inside CI right after the traffic
switch, before the metric observation window starts.

Usage:
    TARGET_URL=https://app.internal python smoke_test.py
"""
import os
import sys
import urllib.error
import urllib.request

TARGET_URL = os.environ.get("TARGET_URL", "http://localhost:8080").rstrip("/")

CHECKS = [
    ("GET", "/", "home page loads"),
    ("GET", "/health", "health endpoint up"),
    ("POST", "/api/session", "session can be created"),
    ("GET", "/api/search?q=phone", "search returns results"),
    ("GET", "/api/cart", "cart state readable"),
]


def run_check(method: str, path: str, label: str) -> tuple[bool, int]:
    req = urllib.request.Request(f"{TARGET_URL}{path}", method=method)
    if method == "POST":
        req.data = b"{}"
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status < 300, resp.status
    except urllib.error.HTTPError as exc:
        return False, exc.code
    except urllib.error.URLError:
        return False, 0


def main() -> int:
    failures = 0
    for method, path, label in CHECKS:
        ok, status = run_check(method, path, label)
        verdict = "PASS" if ok else "FAIL"
        print(f"{verdict} {method} {path} -> {status} ({label})")
        failures += 0 if ok else 1
    if failures:
        print(f"smoke test: {failures} check(s) failed — consider rollback")
        return 1
    print("smoke test: all checks passed on green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
