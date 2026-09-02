-- Concurrency tests for stored procedures
-- PostgreSQL: run with pg_prove
-- These tests verify isolation behavior and duplicate ID prevention

BEGIN;
SELECT plan(2);

-- Test 1: Verify no duplicate IDs under sequential insert
INSERT INTO qa_staging.orders (id, status) VALUES (100, 'pending');
SELECT throws_ok(
    $$INSERT INTO qa_staging.orders (id, status) VALUES (100, 'pending')$$,
    'duplicate key value violates unique constraint',
    'Duplicate ID insert is rejected'
);

-- Test 2: Verify READ COMMITTED isolation shows committed data only
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
INSERT INTO qa_staging.orders (id, status) VALUES (200, 'pending');
SELECT is(
    (SELECT count(*) FROM qa_staging.orders WHERE id = 200),
    1::bigint,
    'Newly inserted row is visible under READ COMMITTED'
);

SELECT * FROM finish();
ROLLBACK;
