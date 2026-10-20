"""Tests for the file-compression-download lab.

Each test maps to a test case in the QAPractices suite
(test-cases/file-compression-download-test-cases).
"""

import io
import zipfile

import pytest

from archive_lab import (
    build_manifest,
    check_unpacked_size,
    create_zip,
    parse_range,
    sanitize_entry,
    serve_download,
    sha256_hex,
    verify_archive,
    zip_entries,
)

FILES = {
    "reports/q1.pdf": b"Q1 report bytes" * 100,
    "reports/q2.pdf": b"Q2 report bytes" * 100,
    "reports/nested/deep.csv": b"a,b,c\n" * 50,
}
MANIFEST = build_manifest(FILES)


def test_single_file_zip_valid():  # TC-001
    one = {"invoice-2026-09.pdf": b"pdf-bytes-2mb-simulated"}
    archive = create_zip(one)
    assert zipfile.is_zipfile(io.BytesIO(archive))
    verify_archive(archive, build_manifest(one))


def test_folder_structure_preserved():  # TC-003
    archive = create_zip(FILES)
    assert set(zip_entries(archive)) == set(FILES)


def test_checksum_match_and_mismatch():  # TC-005
    archive = create_zip(FILES)
    verify_archive(archive, MANIFEST)
    bad = dict(MANIFEST)
    bad["reports/q1.pdf"] = "0" * 64
    with pytest.raises(AssertionError, match="checksum mismatch"):
        verify_archive(archive, bad)


def test_truncated_archive_detected():  # TC-014
    archive = create_zip(FILES)
    partial = archive[: len(archive) * 4 // 5]
    with pytest.raises((zipfile.BadZipFile, AssertionError)):
        verify_archive(partial, MANIFEST)


def test_empty_folder_zip_is_valid():  # TC-016
    archive = create_zip({})
    assert zipfile.is_zipfile(io.BytesIO(archive))
    assert zip_entries(archive) == []


def test_missing_file_returns_404():  # TC-012
    status, headers, _ = serve_download(FILES, "file-0000", "alice", "alice")
    assert status == 404
    assert headers["Content-Type"] == "application/json"


def test_other_users_file_returns_403():  # TC-013
    status, _, body = serve_download(FILES, "reports/q1.pdf", "bob", "alice")
    assert status == 403
    assert FILES["reports/q1.pdf"] not in body


def test_range_resume_returns_206_and_valid_bytes():  # TC-020
    archive = create_zip(FILES)
    store = {"export-1": archive}
    full = len(archive)
    cut = full * 3 // 5  # interrupted at 60%

    status, headers, body = serve_download(
        store, "export-1", "alice", "alice", range_header=f"bytes={cut}-"
    )
    assert status == 206
    assert headers["Content-Range"] == f"bytes {cut}-{full - 1}/{full}"
    reassembled = archive[:cut] + body
    verify_archive(reassembled, MANIFEST)


def test_invalid_range_returns_416():  # edge row: invalid Range
    archive = create_zip(FILES)
    store = {"export-1": archive}
    status, headers, _ = serve_download(
        store, "export-1", "alice", "alice", range_header="bytes=999999999-"
    )
    assert status == 416
    assert headers["Content-Range"] == f"bytes */{len(archive)}"


def test_suffix_range():  # edge: last-N-bytes request
    status, start, end = parse_range("bytes=-100", 1000)
    assert (status, start, end) == (206, 900, 999)


def test_unicode_names_roundtrip():  # TC-022
    files = {"报告.pdf": b"a", "تقرير.pdf": b"b", "résumé 🔥.pdf": b"c"}
    archive = create_zip(files)
    assert set(zip_entries(archive)) == set(files)
    verify_archive(archive, build_manifest(files))


def test_same_name_different_folders_no_collision():  # TC-030
    files = {"q1/report.pdf": b"Q1", "q2/report.pdf": b"Q2"}
    archive = create_zip(files)
    verify_archive(archive, build_manifest(files))


def test_path_traversal_rejected():  # edge row: traversal entry
    with pytest.raises(ValueError, match="unsafe"):
        sanitize_entry("../../etc/passwd")
    assert sanitize_entry("reports/q1.pdf") == "reports/q1.pdf"


def test_zip_bomb_guard():  # TC-017
    compressed_zeroes = b"z" * 10_000_000  # 10 MB of zeros compresses tiny
    archive = create_zip({"bomb.bin": compressed_zeroes})
    assert len(archive) < 100_000  # great ratio — the danger
    with pytest.raises(ValueError, match="cap"):
        check_unpacked_size(archive, max_unpacked=5_000_000)


def test_zip_comment_metadata():  # TC-010
    archive = create_zip(FILES, comment=b"export-2026-10-20-001")
    with zipfile.ZipFile(io.BytesIO(archive)) as zf:
        assert zf.comment == b"export-2026-10-20-001"


def test_download_headers_present():  # TC-008
    status, headers, _ = serve_download(
        {"x.zip": b"data"}, "x.zip", "alice", "alice", download_name="reports-q3"
    )
    assert status == 200
    assert headers["Accept-Ranges"] == "bytes"
    assert headers["Content-Disposition"].endswith('filename="reports-q3.zip"')
    assert headers["Content-Type"] == "application/zip"
