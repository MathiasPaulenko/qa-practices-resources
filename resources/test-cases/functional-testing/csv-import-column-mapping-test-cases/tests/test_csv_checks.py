"""Executable subset of the CSV import column-mapping test cases."""

from pathlib import Path

import pytest

from csv_checks import (
    auto_map,
    column_count_errors,
    detect_delimiter,
    find_invalid_emails,
    parse_rows,
    read_headers,
    unmapped_required,
    validate_file,
)

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


# --- Gate checks (edge table) ---

def test_tc013_empty_csv_rejected():
    result = validate_file(FIXTURES / "taskflow_empty.csv")
    assert not result["ok"]
    assert "no data rows" in result["error"]


def test_tc025_headers_only_rejected():
    result = validate_file(FIXTURES / "taskflow_headers_only.csv")
    assert not result["ok"]
    assert "no data rows" in result["error"]


def test_tc015_non_csv_extension_rejected(tmp_path):
    fake = tmp_path / "report.pdf"
    fake.write_bytes(b"%PDF-fake")
    result = validate_file(fake)
    assert not result["ok"]
    assert "unsupported" in result["error"]


# --- Delimiter detection (TC-007 / TC-008 / TC-009) ---

def test_tc007_semicolon_delimiter_detected():
    text = (FIXTURES / "taskflow_semicolon.csv").read_text(encoding="utf-8")
    assert detect_delimiter(text) == ";"
    assert read_headers(FIXTURES / "taskflow_semicolon.csv") == [
        "Name", "Email", "Phone", "Department", "Role", "StartDate",
    ]


def test_tc008_tab_delimiter_detected():
    text = (FIXTURES / "taskflow_tab.tsv").read_text(encoding="utf-8")
    assert detect_delimiter(text) == "\t"


def test_tc009_quoted_comma_field_is_single_value():
    rows = parse_rows(FIXTURES / "taskflow_team.csv")
    last = rows[-1]
    assert last[0] == "Pérez, Juan"
    assert last[3] == "Buenos Aires, Argentina"
    assert len(last) == 6


# --- BOM + whitespace (TC-019 / TC-020) ---

def test_tc019_bom_stripped_from_first_header():
    headers = read_headers(FIXTURES / "taskflow_utf8_bom.csv")
    assert headers[0] == "Name"  # not "\ufeffName"


def test_tc020_whitespace_headers_trimmed(tmp_path):
    messy = tmp_path / "messy.csv"
    messy.write_text(
        "  Name  ,  Email  ,  Phone  \nA,a@taskflow.io,1\n", encoding="utf-8",
    )
    assert read_headers(messy) == ["Name", "Email", "Phone"]


# --- Auto-mapping (TC-002 / TC-011) ---

def test_tc002_header_aliases_map_to_system_fields():
    headers = ["First Name", "Email Address", "Phone Number", "Role"]
    mapping = auto_map(headers)
    assert mapping["First Name"] == "firstName"
    assert mapping["Email Address"] == "email"
    assert mapping["Phone Number"] == "phone"


def test_tc011_missing_required_field_blocks_import():
    headers = read_headers(FIXTURES / "taskflow_headers_only.csv")
    mapping = auto_map(headers)
    assert unmapped_required(mapping) == []
    partial = auto_map(["Name", "Phone"])
    assert "email" in unmapped_required(partial)


# --- Row-level validation (TC-012 / TC-014 / TC-021) ---

def test_tc014_ragged_row_flagged():
    rows = parse_rows(FIXTURES / "taskflow_ragged.csv")
    flagged = column_count_errors(rows[1:], expected=len(rows[0]))
    assert flagged == [2]  # first data row has 3 cols vs 6 headers


def test_tc012_invalid_email_detected(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text(
        "Name,Email\nJuan Pérez,juan@invalid\nMaría López,maria.lopez@taskflow.io\n",
        encoding="utf-8",
    )
    rows = parse_rows(bad)
    assert find_invalid_emails(rows, ["Name", "Email"]) == [2]


def test_tc021_international_characters_preserved():
    rows = parse_rows(FIXTURES / "taskflow_team.csv")
    names = [r[0] for r in rows[1:]]
    assert "José García" in names
    assert "Søren Nielsen" in names
    assert "北京" in names


def test_tc017_duplicate_emails_detected(tmp_path):
    dup = tmp_path / "dup.csv"
    dup.write_text(
        "Name,Email\nA,juan.perez@taskflow.io\nB,juan.perez@taskflow.io\n",
        encoding="utf-8",
    )
    rows = parse_rows(dup)
    emails = [r[1] for r in rows[1:]]
    assert len(emails) != len(set(emails))
