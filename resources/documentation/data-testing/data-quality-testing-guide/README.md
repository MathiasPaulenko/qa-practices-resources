# Data Quality Guide — Companion Resources

Runnable versions of the checks from the [Data Quality Guide](https://qapractices.com/documentation/data-quality-testing-guide/) on QAPractices.

## Files

| File | What it does |
|---|---|
| `integrity_checks.sql` | Five SQL checks: orphan detection, duplicate keys, a daily profiling query, row-count reconciliation and value-level reconciliation. Run against PostgreSQL 15+; adapt table and column names to your schema. |
| `schema_validation.py` | Python validator using `jsonschema` 4.x that rejects records missing required fields or with wrong types, ready to wire into an ingestion gate. |

## Usage

```bash
# SQL checks (PostgreSQL)
psql -d your_db -f integrity_checks.sql

# Python schema validator
pip install jsonschema
python schema_validation.py
```

## Requirements

- PostgreSQL 15+ (or adapt the SQL to your engine)
- Python 3.11+
- `jsonschema` 4.x
