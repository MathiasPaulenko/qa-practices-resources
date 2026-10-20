# File Compression & Download Lab

Runnable companion for [File Compression & Download Test Cases](https://qapractices.com/test-cases/file-compression-download-test-cases/) — a stdlib-only Python lab that mirrors TaskFlow's export feature: deterministic zip creation, SHA-256 manifest verification, HTTP range semantics (`206 Partial Content` / `416`) and safety guards for path traversal and zip bombs.

## Run

```bash
pip install -r requirements.txt
pytest -v
```

## What it covers

| Test | Suite case |
|---|---|
| `test_single_file_zip_valid` | TC-001 single file as zip |
| `test_folder_structure_preserved` | TC-003 folder structure |
| `test_checksum_match_and_mismatch` | TC-005 checksum verification |
| `test_download_headers_present` | TC-008 download headers |
| `test_zip_comment_metadata` | TC-010 zip comment metadata |
| `test_missing_file_returns_404` | TC-012 non-existent file |
| `test_other_users_file_returns_403` | TC-013 unauthorized download |
| `test_truncated_archive_detected` | TC-014 corrupted zip after drop |
| `test_empty_folder_zip_is_valid` | TC-016 empty folder |
| `test_zip_bomb_guard` | TC-017 zip bomb rejection |
| `test_range_resume_returns_206_and_valid_bytes` | TC-020 resume via Range |
| `test_unicode_names_roundtrip` | TC-022 Unicode filenames |
| `test_same_name_different_folders_no_collision` | TC-030 name collision |
| `test_path_traversal_rejected` | Edge: `../` entries |
| `test_invalid_range_returns_416` / `test_suffix_range` | Edge: range semantics |
