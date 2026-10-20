"""Stdlib validators for report export artifacts.

Covers the checks exercised by the QAPractices test cases TC001, TC007,
TC033-TC037: CSV row counts, UTF-8 BOM, filename sanitization and the
queued/completed async-export contract.
"""

import csv
import json
import re
import unicodedata
from pathlib import Path

UTF8_BOM = b"\xef\xbb\xbf"


def has_utf8_bom(path: str | Path) -> bool:
    """CSV needs a BOM for Excel to render non-Latin text (TC037)."""
    return Path(path).read_bytes()[:3] == UTF8_BOM


def count_data_rows(path: str | Path) -> int:
    """Data rows only, excluding the header (TC001, TC007)."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)
    return max(len(rows) - 1, 0)


def read_csv_rows(path: str | Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def is_sanitized_filename(name: str) -> bool:
    """ASCII-safe, date-stamped filename, no spaces/quotes/separators (TC034)."""
    return bool(re.fullmatch(r"[a-z0-9-_]+_[0-9]{4}-[0-9]{2}-[0-9]{2}\.(csv|pdf|xlsx)", name))


def sanitize_filename(report_name: str) -> str:
    """Produce the sanitized basename InsightFlow should emit, e.g.
    'Revenue "Q2" — Café/Naïve' -> 'revenue-q2-cafe-naive'."""
    ascii_name = (
        unicodedata.normalize("NFKD", report_name)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    return slug or "report"


def parse_export_status(payload: str | bytes) -> dict:
    """Parse a GET /reports/exports/{id} response (TC033).

    Returns {"exportId", "status", "downloadUrl"}; status must be one of
    queued | processing | completed | failed.
    """
    data = json.loads(payload)
    status = data.get("status")
    if status not in {"queued", "processing", "completed", "failed"}:
        raise ValueError(f"unexpected export status: {status!r}")
    if status == "completed" and not data.get("downloadUrl"):
        raise ValueError("completed export must include downloadUrl")
    return {
        "exportId": data.get("exportId"),
        "status": status,
        "downloadUrl": data.get("downloadUrl"),
    }


if __name__ == "__main__":
    fixture = Path(__file__).parent / "fixtures" / "report_q2.csv"
    print("BOM present:", has_utf8_bom(fixture))
    print("Data rows:", count_data_rows(fixture))
    print("Sanitized:", is_sanitized_filename("revenue-q2_2026-07-28.csv"))
    print("From 'Revenue \"Q2\" — Café/Naïve':", sanitize_filename('Revenue "Q2" — Café/Naïve'))
