"""Check a password against the Have I Been Pwned breach corpus.

Uses the k-anonymity model: only the first 5 hex characters of the
SHA-1 hash are sent to the API — the password itself never leaves
the machine.

Usage:
    python breach_check.py "Correct-Horse-Battery-Staple!"
"""

import hashlib
import sys

import requests

HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{prefix}"


def is_breached(password: str) -> bool:
    """Return True if the password appears in the HIBP breach corpus."""
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    resp = requests.get(HIBP_RANGE_URL.format(prefix=prefix), timeout=5)
    resp.raise_for_status()
    return suffix in (line.split(":")[0] for line in resp.text.splitlines())


if __name__ == "__main__":
    candidate = sys.argv[1] if len(sys.argv) > 1 else "password123"
    result = is_breached(candidate)
    print(f"{'BREACHED' if result else 'OK'}: {candidate!r}")
    sys.exit(1 if result else 0)
