"""Replay the carrier webhook fixtures against a tracking endpoint.

Usage:
    python replay_webhooks.py --base-url http://localhost:8000/webhooks/tracking
    python replay_webhooks.py --base-url http://localhost:8000/webhooks/tracking \
        --files 01-label-created.json 02-in-transit.json 06-duplicate-in-transit.json

Each fixture is POSTed as JSON. The script prints the HTTP status per fixture so
you can verify idempotency (duplicate → 200, no state change) and ordering
(delivered followed by late out_for_delivery → status stays delivered).
"""

import argparse
import json
import time
from pathlib import Path

import requests

FIXTURE_DIR = Path(__file__).resolve().parent.parent / "carrier-webhooks"


def load_fixture(name: str) -> dict:
    with open(FIXTURE_DIR / name, encoding="utf-8") as fh:
        payload = json.load(fh)
    payload.pop("_note", None)  # documentation field, not part of the wire payload
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay carrier tracking webhooks")
    parser.add_argument("--base-url", required=True, help="Webhook receiver URL")
    parser.add_argument(
        "--files",
        nargs="*",
        default=[p.name for p in sorted(FIXTURE_DIR.glob("*.json"))],
        help="Fixture filenames in send order (default: all, sorted)",
    )
    parser.add_argument("--delay", type=float, default=0.2, help="Seconds between POSTs")
    args = parser.parse_args()

    for name in args.files:
        payload = load_fixture(name)
        response = requests.post(args.base_url, json=payload, timeout=10)
        print(
            f"{name:42s} -> {response.status_code} "
            f"status={payload['status']} event_id={payload['event_id']}"
        )
        time.sleep(args.delay)


if __name__ == "__main__":
    main()
