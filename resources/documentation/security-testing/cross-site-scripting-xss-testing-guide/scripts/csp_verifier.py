#!/usr/bin/env python3
# csp_verifier.py
# Requires: Python 3.12, requests 2.32
"""Verify CSP headers and test that the policy blocks inline scripts."""
import argparse
import requests


def get_csp(url: str) -> str | None:
    """Return the Content-Security-Policy header value, or None if absent."""
    response = requests.get(url, timeout=10)
    return response.headers.get("Content-Security-Policy")


def evaluate_csp(csp: str) -> list[str]:
    """Return a list of findings about the CSP."""
    findings = []
    if "unsafe-inline" in csp:
        findings.append("WARNING: 'unsafe-inline' is present — inline scripts are allowed")
    if "unsafe-eval" in csp:
        findings.append("WARNING: 'unsafe-eval' is present — eval() is allowed")
    if "script-src 'self'" in csp:
        findings.append("OK: script-src 'self' restricts scripts to same origin")
    if "default-src" not in csp and "script-src" not in csp:
        findings.append("WARNING: no script-src or default-src directive found")
    return findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSP verifier")
    parser.add_argument("--url", required=True, help="Target URL")
    args = parser.parse_args()
    csp = get_csp(args.url)
    if csp is None:
        print(f"[{args.url}] NO CSP HEADER FOUND")
        exit(1)
    print(f"[{args.url}] CSP: {csp}")
    for finding in evaluate_csp(csp):
        print(f"  {finding}")
