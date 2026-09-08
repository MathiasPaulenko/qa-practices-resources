#!/usr/bin/env python3
# reflected_xss_probe.py
# Requires: Python 3.12, requests 2.32
"""Test a search endpoint for reflected XSS by sending a payload and checking if it is reflected unencoded."""
import argparse
import html
import sys
import requests

PAYLOAD = "<script>alert(1)</script>"


def probe(url: str, param: str = "q") -> str:
    """Return one of: REFLECTED_UNENCODED, REFLECTED_ENCODED, NOT_REFLECTED."""
    response = requests.get(url, params={param: PAYLOAD}, timeout=10)
    if PAYLOAD in response.text:
        return "REFLECTED_UNENCODED: payload appears verbatim"
    if html.escape(PAYLOAD) in response.text:
        return "REFLECTED_ENCODED: payload is HTML-escaped"
    return "NOT_REFLECTED"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reflected XSS probe")
    parser.add_argument("--url", required=True, help="Target URL (e.g. https://staging.qa.local/search)")
    parser.add_argument("--param", default="q", help="Query parameter name (default: q)")
    args = parser.parse_args()
    result = probe(args.url, args.param)
    print(f"[{args.url}] {result}")
    if result.startswith("REFLECTED_UNENCODED"):
        sys.exit(1)
