#!/usr/bin/env python3
"""Score regression tests by change impact + history, emit a tiered run list.

Inputs: a changed-files list and a test-history CSV (test,area,last_failed,fails_12w,flake_rate,runtime_s).
Output: tiered run list with a cut line at the time budget.

Usage:
    python3 prioritize_tests.py changed.txt history.csv --budget-min 60
"""
import csv
import sys
from pathlib import Path

WEIGHT_IMPACT = 3.0
WEIGHT_RECENT_FAIL = 2.0
WEIGHT_DENSITY = 1.0
WEIGHT_FLAKE_PENALTY = -1.5


def load_history(path):
    with open(path, newline="") as f:
        yield from csv.DictReader(f)


def impacted_areas(changed_files):
    # map changed path -> test area: top-level module dir, 'shared' if in common dirs
    areas = set()
    for f in changed_files:
        parts = Path(f.strip()).parts
        if not parts:
            continue
        if parts[0] in {"shared", "common", "core", "lib"}:
            areas.add("shared")
        areas.add(parts[0])
    return areas


def score(row, areas):
    impact = WEIGHT_IMPACT if (row["area"] in areas or "shared" in areas) else 0
    recent = WEIGHT_RECENT_FAIL if int(row["last_failed"]) <= 2 else 0
    density = WEIGHT_DENSITY * min(int(row["fails_12w"]), 5) / 5
    flake = WEIGHT_FLAKE_PENALTY if float(row["flake_rate"]) > 0.15 else 0
    return impact + recent + density + flake


def tier(s):
    if s >= 3.5:
        return "must-run"
    if s >= 1.5:
        return "should-run"
    return "can-skip"


def main():
    changed = Path(sys.argv[1]).read_text().splitlines()
    rows = list(load_history(sys.argv[2]))
    budget_s = float(sys.argv[sys.argv.index("--budget-min") + 1]) * 60 if "--budget-min" in sys.argv else 3600

    areas = impacted_areas(changed)
    for r in rows:
        r["score"] = score(r, areas)
        r["tier"] = tier(r["score"])
    rows.sort(key=lambda r: -r["score"])

    spent, cut = 0.0, len(rows)
    for i, r in enumerate(rows):
        if r["tier"] == "can-skip" or spent + float(r["runtime_s"]) > budget_s:
            cut = i
            break
        spent += float(r["runtime_s"])

    for i, r in enumerate(rows):
        mark = "RUN " if i < cut else "SKIP"
        print(f"{mark} [{r['tier']:10s}] {r['score']:+.2f} {r['test']} ({r['runtime_s']}s)")
    print(f"\ncut line after {cut} tests — {spent/60:.1f} min of {budget_s/60:.0f} min budget")


if __name__ == "__main__":
    main()
