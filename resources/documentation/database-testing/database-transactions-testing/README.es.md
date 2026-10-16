# Testing de Transacciones de Base de Datos — Companion

Companion ejecutable de [Cómo Probar Transacciones y Rollbacks de Base de Datos](https://qapractices.com/es/documentation/database-transactions-testing/).

Cinco demos en vivo mapeadas a las secciones de la guía — cada una falla ruidosamente si el comportamiento transaccional se rompe:

| Demo | Qué prueba |
| --- | --- |
| Atomicidad | Un fallo a mitad de transacción no deja escritura parcial |
| Savepoint | `ROLLBACK TO SAVEPOINT` deshace el trabajo posterior, conserva el anterior |
| Optimistic locking | Una escritura con `version` obsoleta es rechazada (protección de lost update) |
| Rollback implícito | Desconectar sin `COMMIT` descarta todo |
| Consistencia | `CHECK (balance >= 0)` aborta una transferencia con sobregiro |

## Archivos

| Archivo | Propósito |
| --- | --- |
| `schema.sql` | Tablas `accounts` + `transfers` con constraints CHECK/FK y columna `version` para optimistic locking. |
| `seed.sql` | Dos cuentas con 100 cada una — estado inicial limpio. |
| `transaction_demos.py` | Las cinco demos; ejecútalo para ver cada comportamiento pasar. |
| `tests/test_transactions.py` | Los mismos comportamientos como casos pytest (7 tests). |

## Uso

```bash
python transaction_demos.py       # corre las demos narradas
pip install -r requirements.txt   # solo pytest
python -m pytest tests/ -v        # corre como suite de tests
```

Requiere Python 3.8+ — `sqlite3` es stdlib, no necesitas servidor de base de datos.

## Notas

- Se eligió SQLite para que las demos corran sin setup. Las secciones de niveles de aislamiento y deadlocks de la guía necesitan un motor cliente-servidor — PostgreSQL o MySQL — donde aplican `SELECT FOR UPDATE`, `deadlock_timeout` y sesiones concurrentes reales.
- La demo de optimistic locking es el patrón, no un sustituto de la implementación de tu ORM (columnas `version` de SQLAlchemy, `@Version` de Hibernate).
- `demo.db` se crea junto al script y se regenera en cada corrida.
