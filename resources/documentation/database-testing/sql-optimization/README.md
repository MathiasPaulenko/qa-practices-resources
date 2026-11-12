# SQL Optimization — Companion

This companion provides runnable files for the [SQL Optimization Guide: Query Plans, Indexes & N+1](https://qapractices.com/documentation/sql-optimization).

## Files

| File | Purpose |
|------|---------|
| `sql/seed-orders.sql` | Builds the `orders` table and seeds 1M rows (scale the `generate_series` bound for 40M) |
| `sql/indexes.sql` | The three index strategies from the guide: composite, covering (`INCLUDE`), partial (`WHERE`) |
| `scripts/benchmark.sh` | Runs N timed executions of a query and reports min/avg/max — the before/after harness |
| `scripts/ci-query-gate.sh` | Fails the pipeline if a benchmarked query exceeds its `Actual Total Time` budget |
| `.github/workflows/query-latency-gate.yml` | GitHub Actions job: Postgres 18 service, seed, gate |

## Quick Start

```bash
# 1. Start PostgreSQL 18 (Docker)
docker run -d --name pg18 -e POSTGRES_PASSWORD=dev -p 5432:5432 postgres:18

# 2. Seed (1M rows — bump generate_series for production-scale)
psql postgresql://postgres:dev@localhost/postgres -f sql/seed-orders.sql

# 3. Baseline benchmark — expect Seq Scan, seconds
./scripts/benchmark.sh 50

# 4. Apply the composite index, re-benchmark — expect Index Scan, ms
psql postgresql://postgres:dev@localhost/postgres -f sql/indexes.sql
./scripts/benchmark.sh 50

# 5. Wire the CI gate
./scripts/ci-query-gate.sh 200   # fail if over 200 ms
```

## Notes

The `parcelhub.example` endpoint is an RFC 2606 placeholder — the guide's
scenario is illustrative, but every script here runs against a real
PostgreSQL instance.

Seed volume: 1M rows keeps the script quick locally. The 40M figure from the
guide is what reproduces the 9-second Seq Scan at production scale — raise
`generate_series(1, 1000000)` accordingly if you have the disk.
