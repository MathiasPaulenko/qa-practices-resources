# SQL Optimization — Companion

Este companion provee archivos ejecutables para la [Guía de Optimización SQL: Planes, Índices y N+1](https://qapractices.com/es/documentation/sql-optimization).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `sql/seed-orders.sql` | Crea la tabla `orders` y siembra 1M de filas (sube el límite de `generate_series` para 40M) |
| `sql/indexes.sql` | Las tres estrategias de índice de la guía: compuesto, covering (`INCLUDE`), parcial (`WHERE`) |
| `scripts/benchmark.sh` | Corre N ejecuciones cronometradas de una consulta y reporta min/avg/max — el harness antes/después |
| `scripts/ci-query-gate.sh` | Falla el pipeline si una consulta del benchmark supera su presupuesto de `Actual Total Time` |
| `.github/workflows/query-latency-gate.yml` | Job de GitHub Actions: servicio Postgres 18, seed, gate |

## Inicio Rápido

```bash
# 1. Levanta PostgreSQL 18 (Docker)
docker run -d --name pg18 -e POSTGRES_PASSWORD=dev -p 5432:5432 postgres:18

# 2. Seed (1M filas — sube generate_series para escala de producción)
psql postgresql://postgres:dev@localhost/postgres -f sql/seed-orders.sql

# 3. Benchmark base — espera Seq Scan, segundos
./scripts/benchmark.sh 50

# 4. Aplica el índice compuesto, re-benchmark — espera Index Scan, ms
psql postgresql://postgres:dev@localhost/postgres -f sql/indexes.sql
./scripts/benchmark.sh 50

# 5. Conecta el gate de CI
./scripts/ci-query-gate.sh 200   # falla si supera 200 ms
```

## Notas

El endpoint `parcelhub.example` es un placeholder de la RFC 2606 — el
escenario de la guía es ilustrativo, pero cada script de aquí corre contra
una instancia real de PostgreSQL.

Volumen del seed: 1M de filas mantiene el script rápido en local. La cifra
de 40M de la guía es la que reproduce el Seq Scan de 9 segundos a escala de
producción — sube `generate_series(1, 1000000)` en consecuencia si tienes el
disco.
