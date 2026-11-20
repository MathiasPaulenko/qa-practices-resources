"""Rollback drill: switch traffic back to blue and verify data consistency.

Simulates the worst case — green already served traffic — by checking
that rows written during the green window are still readable on blue
(the silent schema-drift failure mode the guide warns about).

The script is platform-agnostic: it calls two HTTP endpoints that your
app must expose for the drill, typically implemented as debug routes
enabled only in staging:

    POST /drill/write-marker   -> writes a row, returns {"marker": "..."}
    GET  /drill/read-marker?id -> returns 200 if the row is readable

Usage:
    BLUE_URL=http://localhost:8081 GREEN_URL=http://localhost:8082 \
        python rollback_drill.py
"""
import json
import os
import sys
import time
import urllib.request

BLUE_URL = os.environ.get("BLUE_URL", "http://localhost:8081").rstrip("/")
GREEN_URL = os.environ.get("GREEN_URL", "http://localhost:8082").rstrip("/")
SWITCH_DEADLINE_S = 30


def _post_json(url: str, path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"{url}{path}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def _get_status(url: str, path: str) -> int:
    with urllib.request.urlopen(f"{url}{path}", timeout=10) as resp:
        return resp.status


def main() -> int:
    marker = _post_json(GREEN_URL, "/drill/write-marker", {})["marker"]
    print(f"wrote marker on green: {marker}")

    start = time.monotonic()
    deadline = start + SWITCH_DEADLINE_S
    while True:
        try:
            status = _get_status(BLUE_URL, f"/drill/read-marker?id={marker}")
            if status == 200:
                elapsed = time.monotonic() - start
                print(f"marker readable on blue after {elapsed:.1f}s — PASS")
                return 0
        except Exception:
            pass
        if time.monotonic() >= deadline:
            print(f"marker not readable on blue within {SWITCH_DEADLINE_S}s — FAIL")
            return 1
        time.sleep(1)


if __name__ == "__main__":
    sys.exit(main())
