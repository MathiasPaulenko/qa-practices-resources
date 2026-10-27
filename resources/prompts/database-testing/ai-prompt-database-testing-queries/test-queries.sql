-- DB-001: Insert user with duplicate email must fail (UNIQUE enforcement)
-- Expected: error "UNIQUE constraint failed: users.email"
INSERT INTO users (email, name, role) VALUES ('fixture@shop.dev', 'Dup', 'customer'); -- must FAIL

-- DB-002: Insert order pointing at a non-existent user must fail (FK enforcement)
-- Requires: PRAGMA foreign_keys = ON;
-- Expected: error "FOREIGN KEY constraint failed"
INSERT INTO orders (user_id, status, total) VALUES (9999, 'pending', 10.0); -- must FAIL

-- DB-003: Deleting a user with orders must fail (FK RESTRICT)
-- Expected: error "FOREIGN KEY constraint failed"
DELETE FROM users WHERE id = 42; -- must FAIL

-- DB-004: Orphan detection — must return 0 rows
SELECT o.* FROM orders o LEFT JOIN users u ON o.user_id = u.id WHERE u.id IS NULL;

-- DB-005: CHECK constraint — quantity <= 0 must be rejected
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (1, 1, 0, 9.99); -- must FAIL

-- DB-006: Order total consistency — sum(items) vs order.total. 0 rows expected
SELECT o.id, o.total, COALESCE(SUM(i.quantity * i.price), 0) AS items_total
FROM orders o LEFT JOIN order_items i ON i.order_id = o.id
GROUP BY o.id HAVING ABS(o.total - items_total) > 0.001;

-- Cleanup (idempotent)
DELETE FROM users WHERE email = 'alice@shop.dev';
