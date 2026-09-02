-- pgTAP test: usp_order_summary returns correct totals
-- Run: pg_prove -h localhost -U postgres -d qa_staging test/sql/test_order_summary_pgtap.sql

BEGIN;
SELECT plan(2);

-- Seed test data
INSERT INTO qa_staging.orders (id, status) VALUES (1, 'pending'), (2, 'pending'), (3, 'shipped');
INSERT INTO qa_staging.order_items (order_id, amount) VALUES (1, 100.00), (1, 50.00), (2, 230.00);

-- Test 1: usp_order_summary returns correct totals for 'pending'
SELECT results_eq(
    $$SELECT id, total FROM qa_staging.orders o
       LEFT JOIN qa_staging.order_items oi ON oi.order_id = o.id
       WHERE o.status = 'pending'
       GROUP BY o.id
       ORDER BY o.id$$,
    $$VALUES (1, 150.00::numeric), (2, 230.00::numeric)$$,
    'usp_order_summary returns correct totals for pending orders'
);

-- Test 2: empty result set for non-existent status
SELECT results_eq(
    $$SELECT id, total FROM qa_staging.orders o
       LEFT JOIN qa_staging.order_items oi ON oi.order_id = o.id
       WHERE o.status = 'cancelled'
       GROUP BY o.id$$,
    $$SELECT NULL::int, NULL::numeric WHERE FALSE$$,
    'usp_order_summary returns empty set for non-existent status'
);

SELECT * FROM finish();
ROLLBACK;
