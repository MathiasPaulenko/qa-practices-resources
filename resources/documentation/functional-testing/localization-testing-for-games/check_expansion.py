"""Flag translations that exceed their per-area expansion budget.

Expects a CSV string table exported from a TMS with at least the columns
`key`, `en`, `target` and optionally `ui_area`. Prints one line per string
that exceeds the budgeted length for its UI area.

Usage:
    python check_expansion.py strings_de.csv
"""

import csv
import sys

# Length ratio vs English, per UI area. HUD strings have the least room;
# paragraphs and store copy can take more.
BUDGET = {"default": 1.35, "button": 1.20, "hud": 1.10, "paragraph": 1.50}


def check(csv_path: str):
    """Yield a diagnostic line for each over-budget translation."""
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            src, tgt = row["en"], row["target"]
            kind = row.get("ui_area") or "default"
            limit = len(src) * BUDGET.get(kind, BUDGET["default"])
            if len(tgt) > limit:
                yield f"{row['key']}: {len(tgt)} chars > {int(limit)} budget ({kind})"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python check_expansion.py <string_table.csv>")
    issues = list(check(sys.argv[1]))
    for issue in issues:
        print(issue)
    sys.exit(1 if issues else 0)
