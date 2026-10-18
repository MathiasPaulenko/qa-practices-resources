import pytest

from importer import FormatError, import_csv

VALID = b"name,email,role\nAna Torres,ana@qa-import.test,admin\nBob Lee,bob@qa-import.test,member\n"


def test_valid_file_imports_all_rows():
    rows, report = import_csv(VALID)
    assert report.imported == 2 and report.errors == [] and len(rows) == 2


def test_semicolon_delimiter_rejected():
    with pytest.raises(FormatError):
        import_csv(b"name;email;role\nAna;ana@qa-import.test;admin\n")


def test_utf8_bom_does_not_corrupt_first_header():
    rows, report = import_csv(b"\xef\xbb\xbf" + VALID)
    assert report.imported == 2 and rows[0]["name"] == "Ana Torres"


def test_missing_email_reports_exact_row():
    rows, report = import_csv(
        VALID + b"Empty Email,,admin\n")
    assert report.errors == [{"row": 4, "column": "email",
                              "reason": "required field empty"}]
    assert report.imported == 2


def test_invalid_email_rejected_by_row():
    rows, report = import_csv(
        VALID + b"Carla Diaz,not-an-email,member\n")
    assert report.errors[0]["column"] == "email"
    assert report.errors[0]["row"] == 4


def test_duplicate_email_second_occurrence_flagged():
    data = VALID + b"Dup,dup@qa-import.test,member\nDup2,dup@qa-import.test,member\n"
    rows, report = import_csv(data)
    assert report.errors[0]["row"] == 5 and "duplicate" in report.errors[0]["reason"]
    assert sum(1 for r in rows if r["email"] == "dup@qa-import.test") == 1


def test_header_variants_map_to_canonical():
    for header in (b"First Name", b"first_name", b"FirstName"):
        rows, _ = import_csv(header + b",email,role\nAna,ana@qa-import.test,admin\n")
        assert rows[0]["first_name"] == "Ana"


def test_quoted_commas_and_newlines_stay_one_row():
    data = (b'name,email,role\n"Doe, John",doe@qa-import.test,admin\n'
            b'"Line1\nLine2",line@qa-import.test,member\n')
    rows, report = import_csv(data)
    assert report.imported == 2
    assert rows[0]["name"] == "Doe, John"
    assert "\n" in rows[1]["name"]


def test_blank_rows_skipped_not_errors():
    data = VALID + b"\n\n\n"
    rows, report = import_csv(data)
    assert report.imported == 2 and report.skipped == 3 and report.errors == []


def test_atomic_mode_rolls_back_everything():
    data = VALID + b"Bad,not-an-email,member\n"
    rows, report = import_csv(data, atomic=True)
    assert rows == [] and report.imported == 0 and len(report.errors) == 1


def test_partial_mode_keeps_valid_rows():
    data = VALID + b"Bad,not-an-email,member\n"
    rows, report = import_csv(data)
    assert report.imported == 2 and len(rows) == 2


def test_formula_injection_neutralized():
    data = b"name,email,role\n=cmd|'/c calc'!A1,evil@qa-import.test,member\n"
    rows, _ = import_csv(data)
    assert rows[0]["name"].startswith("'=")


def test_renamed_xlsx_rejected_by_magic_bytes():
    with pytest.raises(FormatError, match="xlsx"):
        import_csv(b"PK\x03\x04" + b"\x00" * 64)


def test_summary_counts_match_reality():
    data = VALID + b"Bad,not-an-email,member\n\n"
    rows, report = import_csv(data)
    assert report.imported == len(rows) == 2
    assert report.skipped == 1 and len(report.errors) == 1
