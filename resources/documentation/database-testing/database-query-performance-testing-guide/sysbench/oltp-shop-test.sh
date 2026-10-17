#!/usr/bin/env bash
# sysbench OLTP read/write load test for MySQL staging.
# Requires sysbench 1.0+ (https://github.com/akopytov/sysbench)
# Usage: DB_HOST=... DB_USER=... DB_PASS=... DB_NAME=shop_db bash sysbench/oltp-shop-test.sh

set -euo pipefail

DB_HOST="${DB_HOST:-db-staging.acme-shop.internal}"
DB_USER="${DB_USER:-qa_user}"
DB_PASS="${DB_PASS:-qa_pass}"
DB_NAME="${DB_NAME:-shop_db}"
TABLES="${TABLES:-10}"
TABLE_SIZE="${TABLE_SIZE:-100000}"
THREADS="${THREADS:-32}"
DURATION="${DURATION:-300}"

echo "==> sysbench prepare (${TABLES} tables x ${TABLE_SIZE} rows)"
sysbench oltp_read_write \
  --mysql-host="${DB_HOST}" \
  --mysql-user="${DB_USER}" \
  --mysql-password="${DB_PASS}" \
  --mysql-db="${DB_NAME}" \
  --tables="${TABLES}" \
  --table-size="${TABLE_SIZE}" \
  prepare

echo "==> sysbench run (${THREADS} threads, ${DURATION}s)"
sysbench oltp_read_write \
  --mysql-host="${DB_HOST}" \
  --mysql-user="${DB_USER}" \
  --mysql-password="${DB_PASS}" \
  --mysql-db="${DB_NAME}" \
  --tables="${TABLES}" \
  --table-size="${TABLE_SIZE}" \
  --threads="${THREADS}" \
  --time="${DURATION}" \
  --report-interval=15 \
  run

echo "==> sysbench cleanup"
sysbench oltp_read_write \
  --mysql-host="${DB_HOST}" \
  --mysql-user="${DB_USER}" \
  --mysql-password="${DB_PASS}" \
  --mysql-db="${DB_NAME}" \
  --tables="${TABLES}" \
  cleanup
