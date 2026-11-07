"""PAN sweep — finds cardholder data leaked into logs, responses, or dumps.

Covers PCI DSS requirement 3: stored PAN must be unreadable and sensitive
authentication data must never be stored post-authorization. Candidate
13-19 digit sequences are validated with the Luhn algorithm to reduce
false positives from order IDs and timestamps.
"""

import re
import sys
from pathlib import Path

PAN_CANDIDATE = re.compile(r"\b\d{13,19}\b")
ALLOWED_SUFFIX = re.compile(r"^\*{6}\d{4}$|^\*{8}\d{4}$|^\d{6}\*{6}\d{4}$")


def luhn_valid(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        total += d if i % 2 == 0 else (d * 2 - 9 if d * 2 > 9 else d * 2)
    return total % 10 == 0


def find_pans(text: str) -> list[str]:
    """Return Luhn-valid PAN candidates found in text."""
    return [m for m in PAN_CANDIDATE.findall(text) if luhn_valid(m)]


def sweep_path(path: Path) -> dict[str, list[str]]:
    """Scan every readable file under path. Returns {file: [pans]}."""
    findings: dict[str, list[str]] = {}
    files = [path] if path.is_file() else sorted(path.rglob("*"))
    for f in files:
        if not f.is_file():
            continue
        try:
            hits = find_pans(f.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        if hits:
            findings[str(f)] = hits
    return findings


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python -m controls.pan_sweep <file-or-dir>")
        return 2
    findings = sweep_path(Path(sys.argv[1]))
    if not findings:
        print("PASS: no Luhn-valid PAN candidates found")
        return 0
    print(f"FAIL: PAN candidates in {len(findings)} file(s)")
    for f, hits in findings.items():
        for h in hits:
            print(f"  {f}: ...{h[-4:]} (masked)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
