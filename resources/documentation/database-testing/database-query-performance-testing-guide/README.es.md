# Companion de Pruebas de Rendimiento de Consultas

Consultas SQL de diagnóstico y un script sysbench ejecutable para la [Guía de Pruebas de Rendimiento de Consultas de Base de Datos](https://qapractices.com/es/documentation/database-query-performance-testing-guide/) de QAPractices.

## Contenido

| Archivo | Qué hace |
|---|---|
| `sql/pg-diagnostics.sql` | Pack de diagnóstico PostgreSQL: consultas top por tiempo acumulado (pg_stat_statements), índices sin usar, lock waits, buffer hit ratio. |
| `sql/explain-orders.sql` | El ejemplo de EXPLAIN ANALYZE de la guía — detecta un índice faltante en una búsqueda de pedidos por usuario. |
| `sysbench/oltp-shop-test.sh` | Carga OLTP lectura/escritura con sysbench 1.0+ contra una base de staging (prepare + run + cleanup). |

## Uso

```bash
# Diagnóstico — ejecútalo contra tu PostgreSQL de staging
psql -h db-staging.acme-shop.internal -U qa_user -d shop_db -f sql/pg-diagnostics.sql

# Ejemplo de índice faltante (siembra orders primero, compara planes antes/después del índice)
psql -h db-staging.acme-shop.internal -U qa_user -d shop_db -f sql/explain-orders.sql

# Load test OLTP — edita host/credenciales primero
bash sysbench/oltp-shop-test.sh
```

## Notas

- `pg-diagnostics.sql` necesita `pg_stat_statements` habilitado (`shared_preload_libraries = 'pg_stat_statements'`).
- Define `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME` antes de correr el script de sysbench.
- Corre siempre los scripts de carga contra staging, nunca contra producción.
