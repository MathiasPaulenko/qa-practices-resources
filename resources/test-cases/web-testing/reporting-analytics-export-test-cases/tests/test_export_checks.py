import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from export_checks import (
    count_data_rows,
    has_utf8_bom,
    is_sanitized_filename,
    parse_export_status,
    read_csv_rows,
    sanitize_filename,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
REPORT = FIXTURES / "report_q2.csv"


def test_csv_has_utf8_bom_for_excel():
    # TC037: BOM present so Excel does not render mojibake.
    assert has_utf8_bom(REPORT)


def test_csv_row_count_excludes_header():
    # TC001: 3 data rows + 1 header line.
    assert count_data_rows(REPORT) == 3


def test_csv_non_latin_values_roundtrip():
    # TC037: non-Latin values survive the CSV round trip unchanged.
    rows = read_csv_rows(REPORT)
    assert rows[0]["customer"] == "田中 太郎"
    assert rows[0]["amount"] == "1234.56"


def test_sanitized_filename_accepted():
    # TC034: ASCII-safe, date-stamped names pass.
    assert is_sanitized_filename("revenue-q2_2026-07-28.csv")


@pytest.mark.parametrize(
    "name",
    [
        'Revenue "Q2" — Café/Naïve.csv',  # spaces, quotes, non-ASCII
        "../escape/report.csv",           # path separator
        "report final.csv",               # space before extension
        "REPORT.CSV",                     # uppercase
        "report_2026-13-99.csv",          # syntactically ok shape, kept for contrast
    ],
)
def test_unsanitized_filenames_rejected(name):
    if name == "report_2026-13-99.csv":
        assert is_sanitized_filename(name)  # pattern is syntactic, not semantic
    else:
        assert not is_sanitized_filename(name)


def test_sanitize_filename_strips_non_ascii():
    assert sanitize_filename('Revenue "Q2" — Café/Naïve') == "revenue-q2-cafe-naive"


def test_queued_status_parses():
    # TC033: 202 Accepted contract returns queued + exportId.
    payload = (FIXTURES / "export_status_queued.json").read_bytes()
    result = parse_export_status(payload)
    assert result["exportId"] == "EXP-3002"
    assert result["status"] == "queued"


def test_completed_status_requires_download_url():
    payload = (FIXTURES / "export_status_completed.json").read_bytes()
    result = parse_export_status(payload)
    assert result["status"] == "completed"
    assert result["downloadUrl"].endswith("/EXP-3002/download")


def test_completed_status_without_url_fails():
    bad = json.dumps({"exportId": "EXP-1", "status": "completed"})
    with pytest.raises(ValueError):
        parse_export_status(bad)


def test_unknown_status_fails():
    bad = json.dumps({"exportId": "EXP-1", "status": "mystery"})
    with pytest.raises(ValueError):
        parse_export_status(bad)
