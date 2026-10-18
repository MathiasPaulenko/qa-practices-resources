"""Minimal CSV importer exercising the failure modes from the test-case suite.

Deliberately dependency-free (stdlib csv): delimiter sniffing, BOM stripping,
header normalization, row-level validation, duplicate detection, partial vs
atomic import, and formula-injection sanitization.
"""

import csv
import io
import re
from dataclasses import dataclass, field

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
HEADER_ALIASES = {"first name": "first_name", "firstname": "first_name",
                  "first_name": "first_name", "name": "name",
                  "email": "email", "e-mail": "email", "role": "role"}
FORMULA_PREFIXES = ("=", "+", "-", "@")


@dataclass
class ImportReport:
    imported: int = 0
    skipped: int = 0
    errors: list = field(default_factory=list)

    def add_error(self, row, column, reason):
        self.errors.append({"row": row, "column": column, "reason": reason})


class FormatError(Exception):
    """Raised when the bytes are not parseable CSV (e.g. a renamed xlsx)."""


def _normalize_header(h):
    return HEADER_ALIASES.get(h.strip().lower(), h.strip().lower().replace(" ", "_"))


def _sanitize(value):
    if value and value[0] in FORMULA_PREFIXES:
        return "'" + value
    return value


def import_csv(raw_bytes, *, atomic=False, seen_emails=None):
    """Import CSV bytes. Returns (rows, ImportReport).

    atomic=False -> valid rows are committed, bad rows reported (partial import).
    atomic=True  -> any error rolls back the entire import.
    """
    if raw_bytes[:4] == b"PK\x03\x04":
        raise FormatError("file is an xlsx (PK magic bytes), not CSV")

    text = raw_bytes.decode("utf-8-sig", errors="strict").replace("\r\n", "\n")
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    if dialect.delimiter != ",":
        raise FormatError(f"unexpected delimiter {dialect.delimiter!r}, expected comma")

    raw = list(csv.reader(io.StringIO(text), dialect=dialect))
    if not raw:
        raise FormatError("empty file")
    fieldnames = [_normalize_header(h) for h in raw[0]]

    report = ImportReport()
    rows, seen = [], set(seen_emails or [])
    for lineno, raw_row in enumerate(raw[1:], start=2):
        if not raw_row or not any(v.strip() for v in raw_row):
            report.skipped += 1
            continue
        row = dict(zip(fieldnames, raw_row))
        email = (row.get("email") or "").strip()
        if not email:
            report.add_error(lineno, "email", "required field empty")
        elif not EMAIL_RE.match(email):
            report.add_error(lineno, "email", "invalid email format")
        elif email in seen:
            report.add_error(lineno, "email", "duplicate email")
        else:
            seen.add(email)
            rows.append({k: _sanitize(v.strip()) for k, v in row.items()
                         if k is not None and v is not None})
            report.imported += 1

    if atomic and report.errors:
        report.imported = 0
        return [], report
    return rows, report
