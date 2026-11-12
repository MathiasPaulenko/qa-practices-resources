"""Scan source files for user-facing strings that bypass the string table.

Matches common UI-text call patterns (setText, AddText, label = "...",
print) with a literal argument instead of a resource lookup. Anything it
finds will stay English in localized builds — that is the defect pseudo-
localization exposes at runtime, but catching it statically is cheaper.

Usage:
    python find_hardcoded_strings.py src/ --ext .cs .gd .cpp
"""

import argparse
import re
import sys
from pathlib import Path

# Calls that put text on screen — adapt to your engine's API.
PATTERN = re.compile(
    r'(?:setText|set_text|AddText|setLabel|label\s*=|Text\s*=|tooltip\s*=)\s*'
    r'\(?\s*["\']([A-Za-z][^"\']{2,})["\']'
)


def scan(path: Path):
    """Yield (file, line_no, string) for each suspicious literal."""
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        m = PATTERN.search(line)
        if m:
            yield path, i, m.group(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--ext", nargs="+", default=[".cs", ".gd", ".cpp", ".ts"])
    args = ap.parse_args()

    hits = [
        hit
        for ext in args.ext
        for f in args.root.rglob(f"*{ext}")
        for hit in scan(f)
    ]
    for path, line_no, text in hits:
        print(f"{path}:{line_no}: {text!r}")
    print(f"\n{len(hits)} candidate hardcoded strings", file=sys.stderr)
