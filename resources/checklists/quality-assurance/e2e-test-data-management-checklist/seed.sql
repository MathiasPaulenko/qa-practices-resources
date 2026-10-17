-- Transactional seed: a failed suite run leaves no partial rows.
-- Run with: psql -d e2e_staging -v ON_ERROR_STOP=1 -f seed.sql
BEGIN;

INSERT INTO users (email, role) VALUES ('qa-seed-01@test.qapractices.dev', 'qa');
INSERT INTO orders (user_id, status)
  VALUES (currval('users_id_seq'), 'pending');
INSERT INTO order_items (order_id, sku, qty)
  VALUES (currval('orders_id_seq'), 'WIDGET-01', 2);

COMMIT;

-- Cleanup counterpart: delete by the deterministic seed prefix
-- DELETE FROM order_items WHERE order_id IN (
--   SELECT id FROM orders WHERE user_id IN (
--     SELECT id FROM users WHERE email LIKE 'qa-seed-%@test.qapractices.dev'));
-- DELETE FROM orders WHERE user_id IN (
--   SELECT id FROM users WHERE email LIKE 'qa-seed-%@test.qapractices.dev');
-- DELETE FROM users WHERE email LIKE 'qa-seed-%@test.qapractices.dev';
