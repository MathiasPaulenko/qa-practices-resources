# Casos de Prueba de Mapeo de Columnas en Import CSV — Companion

Recurso companion de [Casos de Prueba de Mapeo de Columnas en Import CSV](https://qapractices.com/es/test-cases/csv-import-column-mapping-test-cases/).

## Contenido

- `csv_checks.py` — chequeos pre-import en stdlib puro modelados sobre los casos de prueba: lectura `utf-8-sig` (el bug del BOM de TC-019), sniffing de delimitador (`,`/`;`/tab/`|`), normalización de headers + auto-mapping por alias, gateo de campos requeridos, validación de conteo de columnas y emails.
- `fixtures/` — archivos reales, no strings generados: `taskflow_team.csv` (muestra TaskFlow), `taskflow_utf8_bom.csv` (BOM estilo Excel), `taskflow_semicolon.csv`, `taskflow_tab.tsv`, `taskflow_empty.csv`, `taskflow_headers_only.csv`, `taskflow_ragged.csv`.
- `tests/test_csv_checks.py` — 14 tests mapeados a IDs TC: chequeos de gate (vacío / solo-headers / extensión inválida), detección de delimitador, comas entre comillas, eliminación de BOM, trim de whitespace, alias de auto-mapping, bloqueo por campo requerido, filas ragged, emails inválidos, emails duplicados, caracteres i18n.

## Requisitos

- Python 3.10+, `pip install -r requirements.txt` (solo pytest — los chequeos son stdlib)

## Uso

```bash
pytest tests/ -q
```

Salida esperada: `14 passed`.

Los casos a nivel UI (dropdowns de mapeo, resaltado en preview, rollback) corren a nivel de navegador con Playwright 1.48 según las notas de automatización del artículo.

## Relacionados

- Artículo EN: https://qapractices.com/test-cases/csv-import-column-mapping-test-cases/
- Artículo ES: https://qapractices.com/es/test-cases/csv-import-column-mapping-test-cases/
