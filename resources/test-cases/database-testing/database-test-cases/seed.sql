-- Seed schema and fixture for database-test-cases (PostgreSQL 12+)
-- Creates the two-table dataset referenced by all 35 test cases:
-- users(id, name, email) + orders(id, user_id, total, status, created_at)

CREATE TABLE users (
  id    SERIAL PRIMARY KEY,
  name  VARCHAR(200) NOT NULL,
  email VARCHAR(320) NOT NULL UNIQUE
);

CREATE TABLE orders (
  id         SERIAL PRIMARY KEY,
  user_id    INTEGER NOT NULL REFERENCES users(id),
  total      NUMERIC(10,2) NOT NULL CHECK (total >= 0),
  status     VARCHAR(20) NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

INSERT INTO users (id, name, email) VALUES
  (42, 'Ingrid Bergström', 'ingrid.bergstrom@example.com'),
  (99, 'Tariq Mahmoud', 'tariq.mahmoud@example.com'),
  (7, 'Ana Gómez', 'ana.gomez@example.com');

INSERT INTO orders (id, user_id, total, status) VALUES
  (7, 42, 149.90, 'pending');

-- Keep sequences aligned with explicit ids used in the fixture
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('orders_id_seq', (SELECT MAX(id) FROM orders));
