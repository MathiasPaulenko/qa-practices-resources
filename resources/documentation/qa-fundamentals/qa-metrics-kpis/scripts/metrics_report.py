"""Compute defect escape rate and MTTR from a bug-tracker CSV export.

Usage: python scripts/metrics_report.py [path/to/bugs.csv]
Requires: pandas
"""
import sys
from pathlib import Path

import pandas as pd

CSV = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "data" / "bugs.csv"

bugs = pd.read_csv(CSV)

prod_bugs = bugs[bugs["environment"] == "production"]
escape_rate = len(prod_bugs) / len(bugs) * 100
print(f"Defect Escape Rate: {escape_rate:.1f}%  ({len(prod_bugs)}/{len(bugs)} bugs reached production)")

critical = bugs[bugs["priority"].isin(["P1", "P2"])].copy()
critical["open_days"] = (
    pd.to_datetime(critical["closed_date"]) - pd.to_datetime(critical["created_date"])
).dt.days
print(f"MTTR (P1/P2): {critical['open_days'].mean():.1f} days  (n={len(critical)})")
