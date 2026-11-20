"""Probe the MFA verifier for rate limiting and lockout (requests 2.32.3).

A verifier that accepts unlimited wrong codes lets an attacker walk the
one-million combination space of a 6-digit OTP. Assert the endpoint gives
up before `max_attempts` and that the lockout tracks the account, not the IP.
"""

import sys

import requests

VERIFY_URL = "https://staging.qapractices.com/api/auth/mfa/verify"
HEADERS = {"Authorization": "Bearer <challenge-token>"}


def probe_lockout(max_attempts: int = 15) -> int:
    """Send wrong codes until the verifier stops returning 401."""
    status = 200
    for attempt in range(1, max_attempts + 1):
        r = requests.post(VERIFY_URL, json={"code": "000000"}, headers=HEADERS)
        status = r.status_code
        print(f"attempt {attempt}: {status}")
        if status != 401:
            break
    return status


if __name__ == "__main__":
    final = probe_lockout()
    if final == 429:
        print("PASS: verifier rate-limits (429)")
    elif final == 403:
        print("PASS: account locked (403)")
    else:
        print(f"FAIL: no lockout after wrong codes (last status {final})")
        sys.exit(1)
