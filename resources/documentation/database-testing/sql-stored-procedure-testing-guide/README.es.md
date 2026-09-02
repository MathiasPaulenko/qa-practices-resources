# Guía de Testing de Stored Procedures SQL — Companion

Scripts SQL ejecutables para la [Guía de Testing de Stored Procedures SQL](https://qapractices.com/es/documentation/sql-stored-procedure-testing-guide/).

## Contenidos

| Archivo | Framework | Qué testea |
| --- | --- | --- |
| `schema/procedures.sql` | Todos | Stored procedures de ejemplo para SQL Server, PostgreSQL y Oracle |
| `test/sql/test_order_summary_pgtap.sql` | pgTAP | Correctitud de outputs con `results_eq` |
| `test/sql/test_order_summary_tsqlt.sql` | tSQLt | Correctitud de outputs con `AssertEqualsTable` |
| `test/sql/test_input_validation.sql` | Todos | Rechazo de NULL, chequeos de tipo, resistencia a inyección |
| `test/sql/test_error_handling.sql` | Todos | Violaciones PK/FK, deadlocks, rollback on error |
| `test/sql/test_concurrency.sql` | Todos | IDs duplicados, phantom reads, contención de locks |
| `test/sql/test_security.sql` | Todos | Denegación de EXECUTE, ownership chaining |
| `.github/workflows/sql-tests.yml` | GitHub Actions | Pipeline CI con PostgreSQL 16 + pgTAP |

## Quick Start (PostgreSQL + pgTAP)

```bash
# 1. Levantá un contenedor PostgreSQL 16
docker run -d --name qa-pg -e POSTGRES_PASSWORD=qa -e POSTGRES_DB=qa_staging -p 5432:5432 postgres:16

# 2. Instalá pgTAP
docker exec qa-pg bash -c "apt-get update && apt-get install -y postgresql-16-pgtap"

# 3. Cargá el schema y ejecutá los tests
psql -h localhost -U postgres -d qa_staging -f schema/procedures.sql
pg_prove -h localhost -U postgres -d qa_staging test/sql/test_order_summary_pgtap.sql
```

## Quick Start (SQL Server + tSQLt)

```bash
# 1. Levantá un contenedor SQL Server 2022
docker run -d --name qa-sql -e ACCEPT_EULA=Y -e SA_PASSWORD=YourStrong123! -p 1433:1433 mcr.microsoft.com/mssql/server:2022-latest

# 2. Instalá tSQLt (ver https://tsqlt.org/downloads/)
# 3. Cargá el schema y ejecutá los tests
sqlcmd -S localhost -U sa -P YourStrong123! -d qa_staging -i schema/procedures.sql
sqlcmd -S localhost -U sa -P YourStrong123! -d qa_staging -i test/sql/test_order_summary_tsqlt.sql
```

## Integración CI

El archivo `.github/workflows/sql-tests.yml` ejecuta tests de pgTAP en cada push y pull request. Consultá la guía para el setup de CI con SQL Server y Oracle.

## Licencia

MIT — ver el repositorio principal para detalles.
