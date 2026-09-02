-- Error handling tests for stored procedures
-- PostgreSQL: run with pg_prove

BEGIN;
SELECT plan(2);

INSERT INTO qa_staging.accounts (id, balance) VALUES (1, 1000.00), (2, 500.00);

-- Test 1: transfer_funds rolls back on non-existent source account
SELECT throws_ok(
    $$CALL qa_staging.transfer_funds(999, 2, 100.00)$$,
    NULL,
    'transfer_funds throws on non-existent source account'
);

-- Verify balance unchanged after failed transfer
SELECT is(
    (SELECT balance FROM qa_staging.accounts WHERE id = 2),
    500.00::numeric,
    'Account 2 balance unchanged after failed transfer'
);

-- Test 2: transfer_funds handles self-transfer without corruption
SELECT lives_ok(
    $$CALL qa_staging.transfer_funds(1, 1, 50.00)$$,
    'transfer_funds handles self-transfer (net zero)'
);

SELECT is(
    (SELECT balance FROM qa_staging.accounts WHERE id = 1),
    1000.00::numeric,
    'Self-transfer results in net zero balance change'
);

SELECT * FROM finish();
ROLLBACK;
