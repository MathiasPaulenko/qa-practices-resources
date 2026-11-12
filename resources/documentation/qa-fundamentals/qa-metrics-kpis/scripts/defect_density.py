"""Defect density per module (defects per KLOC) from a bug-tracker CSV export.

Usage: python scripts/defect_density.py [path/to/bugs.csv]
The KLOC map below mirrors the guide's module sizes — adjust to your codebase.
"""
import sys
from pathlib import Path

import pandas as pd

CSV = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "data" / "bugs.csv"

KLOC = {"auth": 8, "checkout": 15, "search": 22, "profile": 6}

bugs = pd.read_csv(CSV)
density = bugs.groupby("module").size().rename("defects").to_frame()
density["kloc"] = density.index.map(KLOC)
density["per_kloc"] = density["defects"] / density["kloc"]

print("Density by module:")
for module, row in density.sort_values("per_kloc", ascending=False).iterrows():
    flag = "  <- hotspot" if row["per_kloc"] > 1.0 else ""
    print(f"  {module:<10} {row['per_kloc']:.2f} defects/KLOC ({int(row['defects'])} defects){flag}")
