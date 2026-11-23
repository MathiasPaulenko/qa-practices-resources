# Cómo Realizar Pruebas de Base de Datos con SQL — Companion

Proyecto pytest ejecutable para la guía [Cómo Realizar Pruebas de Base de Datos con SQL](https://qapractices.com/es/documentation/how-to-perform-database-testing-sql) de QAPractices.

## Qué cubre

- `tests/test_crud.py` — verificación de INSERT/UPDATE con `RETURNING id`
- `tests/test_constraints.py` — violaciones de UNIQUE, NOT NULL y FOREIGN KEY verificando `psycopg2.IntegrityError`
- `tests/test_transactions.py` — comportamiento de rollback e integridad `ON DELETE CASCADE`
- `tests/conftest.py` — fixtures `db_connection` y `seeded_users` con setup/teardown automático del schema

## Requisitos

- Python 3.10+
- Una instancia de PostgreSQL dedicada (Docker recomendado): `docker run -e POSTGRES_PASSWORD=test -e POSTGRES_USER=test -e POSTGRES_DB=testdb -p 5432:5432 postgres:16`
- Nunca lo apuntes a producción: el fixture usa variables de entorno (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) con valores de ejemplo.

## Ejecutar

```bash
pip install -r requirements.txt
pytest -v
```
