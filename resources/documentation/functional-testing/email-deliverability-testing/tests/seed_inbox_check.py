#!/usr/bin/env python3
"""Poll a seed mailbox over IMAP and report where a test message landed.

Searches INBOX first, then common spam folder names, for a message whose
Subject contains the token printed by scripts/seed-send.sh. Prints the
placement verdict and the Authentication-Results header when found.

Stdlib only — Python 3.10+.
"""

import argparse
import email
import email.header
import imaplib
import sys
import time

SPAM_CANDIDATES = ["[Gmail]/Spam", "Junk", "Junk Email", "Spam", "INBOX.Spam"]


def decode_subject(raw: str) -> str:
    parts = email.header.decode_header(raw)
    return "".join(
        p.decode(enc or "utf-8", "replace") if isinstance(p, bytes) else p
        for p, enc in parts
    )


def search_folder(conn: imaplib.IMAP4_SSL, folder: str, token: str) -> list[str]:
    status, _ = conn.select(f'"{folder}"', readonly=True)
    if status != "OK":
        return []
    status, data = conn.search(None, "SUBJECT", f'"{token}"')
    if status != "OK" or not data or not data[0]:
        return []
    return data[0].split()


def fetch_headers(conn: imaplib.IMAP4_SSL, msg_id: bytes) -> dict:
    _, data = conn.fetch(msg_id, "(BODY.PEEK[HEADER.FIELDS (AUTHENTICATION-RESULTS SUBJECT)])")
    if not data or not isinstance(data[0], tuple):
        return {}
    msg = email.message_from_bytes(data[0][1])
    return {
        "subject": decode_subject(msg.get("Subject", "")),
        "auth_results": msg.get("Authentication-Results", ""),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", required=True, help="IMAP host, e.g. imap.gmail.com")
    ap.add_argument("--user", required=True, help="Seed account username")
    ap.add_argument("--password", required=True, help="Seed account password or app-password")
    ap.add_argument("--token", required=True, help="Token from seed-send.sh, e.g. deliv-1715000000")
    ap.add_argument("--timeout", type=int, default=120, help="Seconds to poll before giving up")
    args = ap.parse_args()

    deadline = time.time() + args.timeout
    hit = None
    headers = {}

    while time.time() < deadline:
        with imaplib.IMAP4_SSL(args.host) as conn:
            conn.login(args.user, args.password)

            ids = search_folder(conn, "INBOX", args.token)
            if ids:
                hit = ("INBOX", ids[0])
            else:
                for folder in SPAM_CANDIDATES:
                    ids = search_folder(conn, folder, args.token)
                    if ids:
                        hit = (folder, ids[0])
                        break

            if hit:
                headers = fetch_headers(conn, hit[1])
                break
        print("not found yet, retrying in 15s...")
        time.sleep(15)

    if not hit:
        print(f"MISSING: message with token {args.token} did not arrive within {args.timeout}s")
        return 1

    print(f"PLACEMENT: {hit[0]}")
    if headers.get("auth_results"):
        print(f"AUTH-RESULTS: {headers['auth_results']}")

    return 0 if hit[0] == "INBOX" else 2


if __name__ == "__main__":
    sys.exit(main())
