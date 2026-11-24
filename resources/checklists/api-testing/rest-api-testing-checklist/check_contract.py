#!/usr/bin/env python3
"""Check a live REST endpoint against its documented HTTP contract.

Sends a small battery of requests to one route and reports contract
violations: wrong status classes, missing headers, empty error bodies,
non-idempotent writes. Pure stdlib — no dependencies.

Usage:
    python check_contract.py --base http://localhost:8080 --route /users/1 \
        --token $TOKEN --methods GET,PUT,DELETE

Exit code 0 = all checks passed, 1 = violations found.
"""
import argparse
import json
import sys
import urllib.error
import urllib.request


def request(base, route, method, token=None, body=None):
    req = urllib.request.Request(base + route, method=method)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    if body is not None:
        req.add_header("Content-Type", "application/json")
        data = json.dumps(body).encode()
    else:
        data = None
    try:
        with urllib.request.urlopen(req, data=data, timeout=10) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def check_route(base, route, methods, token):
    violations = []

    status, headers, _ = request(base, route, "GET")
    if status >= 500:
        violations.append(f"GET {route} -> {status} (server error on plain read)")

    status, headers, _ = request(base, route, "GET", token="definitely-not-a-token")
    if status != 401:
        violations.append(f"GET {route} with bad token -> {status}, expected 401")

    status, headers, _ = request(base, route, "OPTIONS")
    allow = headers.get("Allow", "")
    if status == 405 and not allow:
        violations.append(f"OPTIONS {route} -> 405 without Allow header")

    status, headers, body = request(base, route, "POST", token=token, body={"__probe": True})
    if 400 <= status < 500 and not body:
        violations.append(f"POST {route} -> {status} with empty error body")
    if status >= 500:
        violations.append(f"POST {route} -> {status} on invalid payload (should be 4xx)")

    if "PUT" in methods:
        probe = {"__idempotent_probe": True}
        s1, _, b1 = request(base, route, "PUT", token=token, body=probe)
        s2, _, b2 = request(base, route, "PUT", token=token, body=probe)
        if s1 != s2 and s1 < 400 and s2 < 400:
            violations.append(
                f"PUT {route} not idempotent: first {s1}, replay {s2}"
            )

    if "DELETE" in methods:
        s1, _, _ = request(base, route, "DELETE", token=token)
        s2, _, _ = request(base, route, "DELETE", token=token)
        if s2 >= 500:
            violations.append(
                f"DELETE {route} second call -> {s2} (repeat delete should be 404/204, not 5xx)"
            )

    return violations


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="Base URL, e.g. http://localhost:8080")
    ap.add_argument("--route", required=True, help="Route path, e.g. /users/1")
    ap.add_argument("--token", default=None, help="Valid bearer token")
    ap.add_argument("--methods", default="GET", help="Comma-separated methods the route documents")
    args = ap.parse_args()

    methods = {m.strip().upper() for m in args.methods.split(",")}
    violations = check_route(args.base, args.route, methods, args.token)

    if violations:
        print(f"CONTRACT VIOLATIONS on {args.route}:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    print(f"{args.route}: contract checks passed")


if __name__ == "__main__":
    main()
