# Identify Performance Bottlenecks — Companion

Runnable artifacts for [How to Identify Performance Bottlenecks](https://qapractices.com/documentation/how-to-identify-performance-bottlenecks/) on QAPractices.

## Contents

| File | Purpose | Related section |
|---|---|---|
| `scripts/k6-load-isolation.js` | Load the app while watching each layer's metrics — the layer that degrades first is the bottleneck | Layered Diagnosis Checklists |
| `scripts/pg_stat_statements-top-queries.sql` | Find the slowest and most frequent PostgreSQL queries | Database Bottlenecks |
| `scripts/web-vitals-rum.js` | Collect real-user LCP/INP/CLS/FCP/TTFB to your metrics endpoint | Frontend Bottlenecks |

## Requirements

- k6 (https://k6.io/docs/get-started/installation/) for the load script.
- PostgreSQL 15+ with `pg_stat_statements` enabled for the SQL file.
- `web-vitals` 4.x installed for the RUM snippet.

## Usage

```bash
# Isolate the layer under load
k6 run scripts/k6-load-isolation.js

# Find slow queries
psql -d yourdb -f scripts/pg_stat_statements-top-queries.sql

# Collect Web Vitals in production
# add scripts/web-vitals-rum.js to your bundle
```

Spanish version: [README.es.md](README.es.md)
