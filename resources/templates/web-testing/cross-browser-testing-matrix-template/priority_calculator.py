"""Browser-matrix priority calculator.

Reads a CSV of browser/OS/viewport combinations with traffic share
percentages and assigns each a P1-P4 priority plus the recommended
test scope — the same decision the priority flow diagram encodes.

Usage:
    python priority_calculator.py traffic-sample.csv
    python priority_calculator.py traffic-sample.csv --p1 30 --p2 5 --p3 2
"""

import argparse
import csv
import sys

DEFAULT_THRESHOLDS = {"P1": 30.0, "P2": 5.0, "P3": 2.0}

SCOPE_BY_PRIORITY = {
    "P1": "Full regression every release (CI) + real-device spot-check",
    "P2": "Smoke plus targeted regression (automated weekly)",
    "P3": "Smoke only (monthly / quarterly)",
    "P4": "Not actively tested (user reports only)",
}


def priority_for(share: float, thresholds: dict) -> str:
    """Map a traffic-share percentage to a priority tier."""
    if share >= thresholds["P1"]:
        return "P1"
    if share >= thresholds["P2"]:
        return "P2"
    if share >= thresholds["P3"]:
        return "P3"
    return "P4"


def assign_priorities(rows: list, thresholds: dict) -> list:
    """Attach priority and scope to each combination row."""
    result = []
    for row in rows:
        share = float(row["traffic_share"])
        prio = priority_for(share, thresholds)
        result.append({**row, "priority": prio, "scope": SCOPE_BY_PRIORITY[prio]})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Assign P1-P4 priorities from traffic share.")
    parser.add_argument("csv_path", help="CSV with traffic_share column")
    parser.add_argument("--p1", type=float, default=DEFAULT_THRESHOLDS["P1"], help="P1 threshold %%")
    parser.add_argument("--p2", type=float, default=DEFAULT_THRESHOLDS["P2"], help="P2 threshold %%")
    parser.add_argument("--p3", type=float, default=DEFAULT_THRESHOLDS["P3"], help="P3 threshold %%")
    args = parser.parse_args()

    thresholds = {"P1": args.p1, "P2": args.p2, "P3": args.p3}
    with open(args.csv_path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    if not rows or "traffic_share" not in rows[0]:
        print("error: CSV must contain a traffic_share column", file=sys.stderr)
        return 1

    writer = csv.DictWriter(sys.stdout, fieldnames=[*rows[0].keys(), "priority", "scope"])
    writer.writeheader()
    for row in assign_priorities(rows, thresholds):
        writer.writerow(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
