-- ENGINE: PostgreSQL 16.4
-- SCHEMA (DDL):
CREATE TABLE users (
  id bigint PRIMARY KEY,
  email varchar(255) NOT NULL,
  tenant_id bigint NOT NULL REFERENCES tenants(id)
);
CREATE TABLE orders (
  id bigint PRIMARY KEY,
  user_id bigint NOT NULL REFERENCES users(id),
  status varchar(20),
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_orders_user ON orders(user_id);
-- row counts: users 120k, orders 5M

-- QUERY TO VALIDATE:
SELECT * FROM orders o, users u
WHERE o.user_id = u.id
  AND u.email LIKE '%@acme.com'
  AND YEAR(o.created_at) = 2026
  AND o.status != 'cancelled'
ORDER BY o.created_at;

-- CONTEXT: admin report endpoint, ~10 req/min, p95 < 500 ms,
-- parameters bound via string interpolation
