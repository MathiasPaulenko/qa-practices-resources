# SQL Stored Procedure Testing Guide — Companion

Runnable SQL test scripts for the [SQL Stored Procedure Testing Guide](https://qapractices.com/documentation/sql-stored-procedure-testing-guide/).

## Contents

| File | Framework | What it tests |
| --- | --- | --- |
| `schema/procedures.sql` | All | Sample stored procedures for SQL Server, PostgreSQL and Oracle |
| `test/sql/test_order_summary_pgtap.sql` | pgTAP | Output correctness with `results_eq` |
| `test/sql/test_order_summary_tsqlt.sql` | tSQLt | Output correctness with `AssertEqualsTable` |
| `test/sql/test_input_validation.sql` | All | NULL rejection, type checks, injection resistance |
| `test/sql/test_error_handling.sql` | All | PK/FK violations, deadlocks, rollback on error |
| `test/sql/test_concurrency.sql` | All | Duplicate IDs, phantom reads, lock contention |
| `test/sql/test_security.sql` | All | EXECUTE permission denial, ownership chaining |
| `.github/workflows/sql-tests.yml` | GitHub Actions | CI pipeline with PostgreSQL 16 + pgTAP |

## Quick Start (PostgreSQL + pgTAP)

```bash
# 1. Start a PostgreSQL 16 container
docker run -d --name qa-pg -e POSTGRES_PASSWORD=qa -e POSTGRES_DB=qa_staging -p 5432:5432 postgres:16

# 2. Install pgTAP
docker exec qa-pg bash -c "apt-get update && apt-get install -y postgresql-16-pgtap"

# 3. Load schema and run tests
psql -h localhost -U postgres -d qa_staging -f schema/procedures.sql
pg_prove -h localhost -U postgres -d qa_staging test/sql/test_order_summary_pgtap.sql
```

## Quick Start (SQL Server + tSQLt)

```bash
# 1. Start a SQL Server 2022 container
docker run -d --name qa-sql -e ACCEPT_EULA=Y -e SA_PASSWORD=YourStrong123! -p 1433:1433 mcr.microsoft.com/mssql/server:2022-latest

# 2. Install tSQLt (see https://tsqlt.org/downloads/)
# 3. Load schema and run tests
sqlcmd -S localhost -U sa -P YourStrong123! -d qa_staging -i schema/procedures.sql
sqlcmd -S localhost -U sa -P YourStrong123! -d qa_staging -i test/sql/test_order_summary_tsqlt.sql
```

## CI Integration

The `.github/workflows/sql-tests.yml` file runs pgTAP tests on every push and pull request. See the guide for SQL Server and Oracle CI setup.

## License

MIT — see the main repository for details.
