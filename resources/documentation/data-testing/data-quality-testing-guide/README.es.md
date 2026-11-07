# Guía de Calidad de Datos — Recursos Complementarios

Versiones ejecutables de los checks de la [Guía de Calidad de Datos](https://qapractices.com/es/documentation/data-quality-testing-guide/) en QAPractices.

## Archivos

| Archivo | Qué hace |
|---|---|
| `integrity_checks.sql` | Cinco checks SQL: detección de huérfanos, claves duplicadas, query de profiling diario, reconciliación de conteos y reconciliación a nivel de valor. Ejecuta contra PostgreSQL 15+; adapta nombres de tablas y columnas a tu schema. |
| `schema_validation.py` | Validador Python con `jsonschema` 4.x que rechaza registros sin campos requeridos o con tipos incorrectos, listo para integrar en una puerta de ingesta. |

## Uso

```bash
# Checks SQL (PostgreSQL)
psql -d tu_db -f integrity_checks.sql

# Validador de schema en Python
pip install jsonschema
python schema_validation.py
```

## Requisitos

- PostgreSQL 15+ (o adapta el SQL a tu motor)
- Python 3.11+
- `jsonschema` 4.x
