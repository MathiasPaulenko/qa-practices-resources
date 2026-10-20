# Testing de Exportación de Reportes y Analítica — Companion

Recurso companion de [Casos de Prueba: Reportes y Exportación de Analítica](https://qapractices.com/es/test-cases/reporting-analytics-export-test-cases/).

## Contenido

- `export_checks.py` — validadores solo stdlib para los artefactos que produce una exportación: detección de BOM UTF-8, conteo de filas CSV excluyendo encabezado, sanitización de nombres de archivo (ASCII-safe, con fecha) y parseo del contrato de exportación asíncrona queued/completed.
- `tests/test_export_checks.py` — suite pytest 8.3 que ejercita los validadores contra los modos de fallo que cubre el artículo: mojibake en Excel (TC037), conteo de filas (TC001/TC007), casos límite de nombres de archivo (TC034) y el payload de estado asíncrono (TC033).
- `fixtures/report_q2.csv` — CSV con prefijo BOM y datos de cliente no latinos.
- `fixtures/export_status_*.json` — los payloads queued y completed del ejemplo asíncrono del artículo.

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
cd resources/test-cases/web-testing/reporting-analytics-export-test-cases
pytest tests/ -v
```

Chequeo manual rápido:

```bash
python export_checks.py
# BOM present: True
# Data rows: 3
# Sanitized: True
# From 'Revenue "Q2" — Café/Naïve': revenue-q2-cafe-naive
```

## Qué cubre

- Integridad CSV: BOM, exclusión del encabezado, round trip de caracteres no latinos (TC001, TC037).
- Reglas de nombre de archivo: slugs ASCII-safe con fecha (TC034).
- Contrato asíncrono: `queued` → `completed` + `downloadUrl`, payloads inválidos rechazados (TC033).
- Valores límite en nombres de archivo: separadores de ruta, espacios, extensiones en mayúsculas.
