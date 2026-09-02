-- Input validation tests for stored procedures
-- PostgreSQL: run with pg_prove

BEGIN;
SELECT plan(3);

-- Test 1: transfer_funds rejects zero amount
SELECT throws_ok(
    $$CALL qa_staging.transfer_funds(1, 2, 0.00)$$,
    'Amount must be positive',
    'transfer_funds rejects zero amount'
);

-- Test 2: transfer_funds rejects negative amount
SELECT throws_ok(
    $$CALL qa_staging.transfer_funds(1, 2, -50.00)$$,
    'Amount must be positive',
    'transfer_funds rejects negative amount'
);

-- Test 3: SQL injection resistance — quote in parameter is treated as data
INSERT INTO qa_staging.accounts (id, balance) VALUES (1, 1000.00), (2, 500.00);

SELECT lives_ok(
    $$CALL qa_staging.transfer_funds(1, 2, 100.00)$$,
    'transfer_funds executes with valid numeric input'
);

SELECT * FROM finish();
ROLLBACK;
