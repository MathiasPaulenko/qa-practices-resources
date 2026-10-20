# Lab de Compresión y Descarga de Archivos

Companion ejecutable de [Casos de Prueba de Compresión y Descarga](https://qapractices.com/es/test-cases/file-compression-download-test-cases/) — un lab en Python solo-stdlib que refleja la exportación de TaskFlow: creación de zips determinista, verificación de manifiesto con SHA-256, semántica HTTP de rangos (`206 Partial Content` / `416`) y guardas contra path traversal y zip bombs.

## Ejecutar

```bash
pip install -r requirements.txt
pytest -v
```

## Qué cubre

| Test | Caso de la suite |
|---|---|
| `test_single_file_zip_valid` | TC-001 archivo único como zip |
| `test_folder_structure_preserved` | TC-003 estructura de carpetas |
| `test_checksum_match_and_mismatch` | TC-005 verificación de checksum |
| `test_download_headers_present` | TC-008 headers de descarga |
| `test_zip_comment_metadata` | TC-010 comentario del zip |
| `test_missing_file_returns_404` | TC-012 archivo inexistente |
| `test_other_users_file_returns_403` | TC-013 descarga sin permisos |
| `test_truncated_archive_detected` | TC-014 zip corrupto tras corte |
| `test_empty_folder_zip_is_valid` | TC-016 carpeta vacía |
| `test_zip_bomb_guard` | TC-017 rechazo de zip bomb |
| `test_range_resume_returns_206_and_valid_bytes` | TC-020 reanudación con Range |
| `test_unicode_names_roundtrip` | TC-022 nombres Unicode |
| `test_same_name_different_folders_no_collision` | TC-030 colisión de nombres |
| `test_path_traversal_rejected` | Edge: entradas `../` |
| `test_invalid_range_returns_416` / `test_suffix_range` | Edge: semántica de rangos |
