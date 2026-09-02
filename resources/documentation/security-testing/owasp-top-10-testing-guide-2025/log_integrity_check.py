"""Log integrity check script for OWASP A09 testing.

Verifies HMAC signatures on log lines to detect tampering.
Requires Python 3.10+ and the `hmac` stdlib.
"""

import hmac
import hashlib
import sys
import os
from pathlib import Path
from typing import Optional


def verify_log_integrity(log_path: str, secret: Optional[str] = None) -> dict:
    """Verify HMAC signatures on each line of a log file.

    Args:
        log_path: Path to the log file to verify.
        secret: HMAC secret key. If None, reads from LOG_HMAC_SECRET env var.

    Returns:
        Dict with 'total_lines', 'verified', 'failed', 'tampered_lines'.
    """
    if secret is None:
        secret = os.environ.get("LOG_HMAC_SECRET")
    if not secret:
        raise ValueError(
            "No HMAC secret provided. Set LOG_HMAC_SECRET env var or pass secret parameter."
        )

    secret_bytes = secret.encode("utf-8")
    path = Path(log_path)

    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {log_path}")

    results = {
        "total_lines": 0,
        "verified": 0,
        "failed": 0,
        "tampered_lines": [],
    }

    with path.open("r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line:
                continue

            results["total_lines"] += 1

            # Expected format: <timestamp>|<event>|<payload>|hmac=<signature>
            parts = line.rsplit("|hmac=", 1)
            if len(parts) != 2:
                results["failed"] += 1
                results["tampered_lines"].append(
                    {"line": line_num, "reason": "no_hmac_field"}
                )
                continue

            log_content, signature = parts[0], parts[1]
            expected = hmac.new(
                secret_bytes, log_content.encode("utf-8"), hashlib.sha256
            ).hexdigest()

            if hmac.compare_digest(signature, expected):
                results["verified"] += 1
            else:
                results["failed"] += 1
                results["tampered_lines"].append(
                    {"line": line_num, "reason": "signature_mismatch"}
                )

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python log_integrity_check.py <log_file> [secret]")
        sys.exit(1)

    log_path = sys.argv[1]
    secret = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        results = verify_log_integrity(log_path, secret)
        print(f"Log integrity check for: {log_path}")
        print(f"  Total lines: {results['total_lines']}")
        print(f"  Verified:     {results['verified']}")
        print(f"  Failed:       {results['failed']}")

        if results["tampered_lines"]:
            print(f"\n  Tampered lines:")
            for entry in results["tampered_lines"][:10]:
                print(f"    Line {entry['line']}: {entry['reason']}")

        if results["failed"] > 0:
            print("\n  RESULT: FAIL — tampering detected")
            sys.exit(1)
        else:
            print("\n  RESULT: PASS — all lines verified")
            sys.exit(0)

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
