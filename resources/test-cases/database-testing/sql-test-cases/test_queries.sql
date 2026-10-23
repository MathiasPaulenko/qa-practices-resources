-- Runnable queries for the SQL Test Cases suite (TC-001 .. TC-007).
-- Engine: MySQL 8.x. PostgreSQL notes inline where syntax differs.
--
--   mysql -u qa -h staging.db.urbanthreads.com -D urbanthreads < test_queries.sql

-- ---------------------------------------------------------------------------
-- TC-001: Valid SELECT returns expected data
-- Expect: 2 rows, customer_id 101 and 103.
-- ---------------------------------------------------------------------------
SELECT * FROM customers WHERE status = 'active';

-- ---------------------------------------------------------------------------
-- TC-002: SQL injection payloads arrive as bound literals, never as SQL.
-- Submit each string through the app; on the wire the query log must show the
-- payload bound to a placeholder, e.g. WHERE email = ?
-- ---------------------------------------------------------------------------
SELECT * FROM customers WHERE email = ''' OR ''1''=''1';
SELECT * FROM customers WHERE email = ''' UNION SELECT * FROM users';
SELECT * FROM customers WHERE email = '''; DROP TABLE customers;';

-- ---------------------------------------------------------------------------
-- TC-003: Transaction atomicity and rollback.
-- Expect: customer 101 back at 250.00, customer 102 still 75.00.
-- ---------------------------------------------------------------------------
BEGIN;
UPDATE store_credit SET balance = balance - 89.99 WHERE customer_id = 101;
SELECT balance FROM store_credit WHERE customer_id = 101;  -- 160.01
-- Force a foreign-key violation with an invalid product_id.
-- INSERT INTO order_items (order_id, product_id, quantity, unit_price)
--   VALUES (1, 'nonexistent-sku', 1, 0.00);
ROLLBACK;
SELECT customer_id, balance FROM store_credit WHERE customer_id IN (101, 102);

-- ---------------------------------------------------------------------------
-- TC-004: Concurrent update handling.
-- Run session A and B in two separate clients; do not mix them in one file.
-- ---------------------------------------------------------------------------
-- Session A:
--   BEGIN;
--   UPDATE inventory SET stock_count = stock_count - 2
--    WHERE product_id = 'retro-denim-jacket';
-- Session B (blocks under pessimistic locking, errors under optimistic):
--   BEGIN;
--   UPDATE inventory SET stock_count = stock_count - 3
--    WHERE product_id = 'retro-denim-jacket';
-- Session A: COMMIT;
-- Final check:
SELECT stock_count FROM inventory WHERE product_id = 'retro-denim-jacket';  -- 5

-- ---------------------------------------------------------------------------
-- TC-005: Large result set and keyset pagination.
-- Expect: EXPLAIN uses idx_tx_keyset, page completes < 200 ms.
-- ---------------------------------------------------------------------------
SELECT *
  FROM transactions
 WHERE status = 'completed'
 ORDER BY created_at DESC, transaction_id DESC
 LIMIT 100 OFFSET 0;

SELECT *
  FROM transactions
 WHERE status = 'completed'
   AND (created_at < '2026-07-25 14:30:00'
        OR (created_at = '2026-07-25 14:30:00' AND transaction_id < 999950))
 ORDER BY created_at DESC, transaction_id DESC
 LIMIT 100;

-- ---------------------------------------------------------------------------
-- TC-006: Stored procedure validation.
-- Expect: order created, stock 10 -> 9, audit row written.
-- ---------------------------------------------------------------------------
CALL sp_CreateOrder(101, 'retro-denim-jacket', 1);
SELECT * FROM orders ORDER BY order_id DESC LIMIT 1;
SELECT stock_count FROM inventory WHERE product_id = 'retro-denim-jacket';
SELECT * FROM order_audit ORDER BY audit_id DESC LIMIT 1;

-- Invalid customer — expect controlled error, no writes.
-- CALL sp_CreateOrder(99999, 'retro-denim-jacket', 1);
-- Zero quantity — expect validation error before any write.
-- CALL sp_CreateOrder(101, 'retro-denim-jacket', 0);

-- ---------------------------------------------------------------------------
-- TC-007: Index effectiveness.
-- Expect: idx_customers_email used; phone_number scans until indexed.
-- ---------------------------------------------------------------------------
EXPLAIN SELECT * FROM customers WHERE email = 'alice@urbanthreads.com';
EXPLAIN SELECT * FROM customers WHERE phone_number = '+1-555-123-4567';

-- CREATE INDEX idx_customers_phone ON customers(phone_number);
-- DROP INDEX idx_customers_phone ON customers;

-- Covering index scenario: no table access needed.
EXPLAIN SELECT email, status FROM customers WHERE status = 'active';
