"""Parse a zap-baseline.py markdown report and fail on high-risk alerts.

Usage:
    python parse_baseline.py zap-baseline.md

Exit code 1 when the report contains any HIGH risk alert, 0 otherwise —
suitable as a CI quality gate step. Stdlib only.
"""

import re
import sys
from collections import Counter

RISK_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(High|Medium|Low|Informational)\s*\|", re.IGNORECASE)


def count_risks(report_text: str) -> Counter:
    counts: Counter = Counter()
    for line in report_text.splitlines():
        match = RISK_ROW.match(line)
        if match:
            counts[match.group(2).lower()] += 1
    return counts


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    text = open(sys.argv[1], encoding="utf-8").read()
    counts = count_risks(text)
    for level in ("high", "medium", "low", "informational"):
        print(f"{level.capitalize()}: {counts[level]}")
    if counts["high"]:
        print("FAIL: high-risk alerts present")
        return 1
    print("PASS: no high-risk alerts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
