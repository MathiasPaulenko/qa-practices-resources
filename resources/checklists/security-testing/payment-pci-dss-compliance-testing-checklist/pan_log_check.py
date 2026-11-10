"""Scan files or directories for PAN (card number) leaks in logs and dumps.

Finds 13-19 digit sequences (ignoring separators), validates them with the
Luhn algorithm, and reports file:line matches. Intended to verify checklist
section 1 items: "PAN never stored in plain text" and "Full PAN never
appears in error messages / logs".

Usage:
    python pan_log_check.py path/to/logs/
    python pan_log_check.py app.log --quiet

Stdlib only. Exit code 1 if candidates are found, 0 if clean.
"""

import argparse
import re
import sys
from pathlib import Path

# 13-19 digits, optionally separated by spaces or dashes in groups of 4
CANDIDATE = re.compile(r"\b(?:\d[ -]?){13,19}\b")
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".zip", ".gz", ".pyc", ".exe"}
# Well-known test card prefixes that should not count as findings
TEST_PREFIXES = ("4242424242424242", "4000000000000002", "5555555555554444", "378282246310005")


def luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def is_test_card(digits: str) -> bool:
    return any(digits.startswith(p) for p in TEST_PREFIXES)


def iter_files(path: Path):
    if path.is_file():
        yield path
        return
    for p in sorted(path.rglob("*")):
        if p.is_file() and p.suffix.lower() not in SKIP_SUFFIXES:
            yield p


def scan_file(path: Path):
    findings = []
    try:
        for n, line in enumerate(path.open(encoding="utf-8", errors="replace"), 1):
            for m in CANDIDATE.finditer(line):
                digits = re.sub(r"\D", "", m.group(0))
                if 13 <= len(digits) <= 19 and luhn_ok(digits) and not is_test_card(digits):
                    findings.append((n, digits[:6] + "*" * (len(digits) - 10) + digits[-4:]))
    except OSError:
        pass
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path, help="File or directory to scan")
    ap.add_argument("--quiet", action="store_true", help="Only print the summary line")
    args = ap.parse_args()

    files = list(iter_files(args.path))
    total = 0
    for f in files:
        for line_no, masked in scan_file(f):
            total += 1
            if not args.quiet:
                print(f"POSSIBLE PAN  {f}:{line_no}  {masked}")

    if total:
        print(f"\n{total} possible PAN leak(s) in {len(files)} scanned file(s). "
              "Verify context and treat as Req 3 findings until proven false positives.")
        return 1
    print(f"Clean: no Luhn-valid card numbers found in {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
