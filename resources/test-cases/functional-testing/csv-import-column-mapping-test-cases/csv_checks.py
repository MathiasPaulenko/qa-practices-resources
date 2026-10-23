"""CSV import checks modeled after the test cases on qapractices.com.

Pure stdlib — implements the pre-import validations the suite verifies:
BOM stripping, delimiter detection, header normalization, column-count
consistency, required-field presence, email format, and empty-file /
headers-only detection.
"""

import csv
import re
from pathlib import Path

ALLOWED_EXTENSIONS = {".csv", ".tsv", ".txt"}
REQUIRED_FIELDS = {"firstName", "email"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

HEADER_ALIASES = {
    "name": "firstName",
    "first name": "firstName",
    "email": "email",
    "email address": "email",
    "phone": "phone",
    "phone number": "phone",
    "department": "department",
    "role": "role",
    "startdate": "startDate",
    "start date": "startDate",
}


def read_text(path: Path | str) -> str:
    """Read with utf-8-sig so a UTF-8 BOM is stripped automatically
    (the TC-019 bug: `\uFEFFName` silently breaking auto-mapping)."""
    return Path(path).read_text(encoding="utf-8-sig")


def detect_delimiter(sample: str) -> str:
    """Detect the delimiter via csv.Sniffer with fallback to comma."""
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
    except csv.Error:
        return ","


def read_headers(path: Path | str) -> list[str]:
    """Return normalized (trimmed) headers, BOM-free."""
    text = read_text(path)
    first_line = text.splitlines()[0] if text.splitlines() else ""
    delimiter = detect_delimiter(text)
    return [h.strip() for h in first_line.split(delimiter)]


def auto_map(headers: list[str]) -> dict[str, str | None]:
    """Map CSV headers to system fields by normalized name."""
    return {h: HEADER_ALIASES.get(h.lower()) for h in headers}


def unmapped_required(mapping: dict[str, str | None]) -> list[str]:
    """System required fields that no header mapped to — blocks import."""
    mapped = set(mapping.values())
    return sorted(REQUIRED_FIELDS - mapped)


def column_count_errors(rows: list[list[str]], expected: int) -> list[int]:
    """1-based row numbers whose column count differs from the header row."""
    return [i + 2 for i, row in enumerate(rows) if len(row) != expected]


def parse_rows(path: Path | str) -> list[list[str]]:
    text = read_text(path)
    delimiter = detect_delimiter(text)
    return list(csv.reader(text.splitlines(), delimiter=delimiter))


def validate_file(path: Path | str) -> dict:
    """Gate checks run before the mapping screen: extension, empty file,
    headers-only file."""
    p = Path(path)
    if p.suffix.lower() not in ALLOWED_EXTENSIONS:
        return {"ok": False, "error": f"unsupported file type: {p.suffix}"}
    rows = parse_rows(p)
    if not rows:
        return {"ok": False, "error": "file contains no data rows"}
    if len(rows) == 1:
        return {"ok": False, "error": "file contains headers but no data rows"}
    return {"ok": True, "rows": rows}


def find_invalid_emails(rows: list[list[str]], headers: list[str]) -> list[int]:
    """1-based data-row numbers with a malformed email."""
    try:
        email_idx = next(
            i for i, h in enumerate(headers)
            if HEADER_ALIASES.get(h.lower()) == "email"
        )
    except StopIteration:
        return []
    return [
        i for i, row in enumerate(rows[1:], start=2)
        if email_idx < len(row) and not EMAIL_RE.match(row[email_idx])
    ]
