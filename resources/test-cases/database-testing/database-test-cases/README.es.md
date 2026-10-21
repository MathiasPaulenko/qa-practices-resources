# Casos de Prueba de Base de Datos — Companion

Artefactos ejecutables para la suite [Casos de Prueba de Base de Datos](https://qapractices.com/es/test-cases/database-test-cases) (35 casos sobre el dataset `users`/`orders`).

## Archivos

| Archivo | Qué hace |
|---|---|
| `seed.sql` | Crea el esquema y el fixture que referencian los 35 casos (PostgreSQL 12+). |
| `validate.sql` | Verificaciones post-migración: constraints, filas huérfanas, NULLs, totales negativos. |
| `test_injection.py` | Suite pytest que prueba que el patrón de consulta parametrizada resiste el payload clásico `' OR '1'='1` — corre sobre SQLite en memoria, sin servidor. |

## Uso

```bash
# Sembrar una base de staging
psql -d staging_db -f seed.sql

# Validación post-migración
psql -d staging_db -f validate.sql

# Verificación de inyección (pytest 8.3+, Python 3.10+)
pip install pytest
pytest test_injection.py -v
```

El test de Python usa SQLite en memoria y corre en cualquier máquina. En PostgreSQL aplica el mismo principio: parámetros vinculados, nunca interpolar input del usuario en cadenas SQL.

Volver a la guía: [qapractices.com/es/test-cases/database-test-cases](https://qapractices.com/es/test-cases/database-test-cases)
