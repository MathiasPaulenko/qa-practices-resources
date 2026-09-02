-- Security and permissions tests for stored procedures
-- PostgreSQL: run with pg_prove
-- Requires a qa_readonly role to be created first:
--   CREATE ROLE qa_readonly LOGIN PASSWORD 'qa_readonly';

BEGIN;
SELECT plan(2);

-- Test 1: Verify that EXECUTE permission can be granted and revoked
-- (Run as superuser in test environment)
SELECT lives_ok(
    $$GRANT USAGE ON SCHEMA qa_staging TO PUBLIC$$,
    'USAGE on schema can be granted'
);

-- Test 2: Verify that a role without EXECUTE cannot call the procedure
-- Create a test role and verify denial
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'qa_readonly') THEN
        CREATE ROLE qa_readonly LOGIN PASSWORD 'qa_readonly';
    END IF;
END $$;

REVOKE EXECUTE ON PROCEDURE qa_staging.transfer_funds(INT, INT, DECIMAL) FROM qa_readonly;

SELECT throws_ok(
    $$SET ROLE qa_readonly; CALL qa_staging.transfer_funds(1, 2, 100.00); RESET ROLE$$,
    'permission denied',
    'Role without EXECUTE cannot call procedure'
);

SELECT * FROM finish();
ROLLBACK;
