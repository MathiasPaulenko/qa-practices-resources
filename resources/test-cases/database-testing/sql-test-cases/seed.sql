-- UrbanThreads seed data — MySQL 8.x dialect.
-- For PostgreSQL 16, replace ENUM with VARCHAR + CHECK and AUTO_INCREMENT with
-- GENERATED ALWAYS AS IDENTITY.
--
-- Usage:
--   mysql -u qa -h staging.db.urbanthreads.com -D urbanthreads < seed.sql

DROP TABLE IF EXISTS order_audit;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS store_credit;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS users;

CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  name        VARCHAR(255) NOT NULL,
  email       VARCHAR(254) NOT NULL,
  status      ENUM('active','inactive') NOT NULL DEFAULT 'active',
  phone_number VARCHAR(32),
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY idx_customers_email (email)
);

CREATE TABLE products (
  product_id  VARCHAR(64) PRIMARY KEY,
  name        VARCHAR(255) NOT NULL,
  price       DECIMAL(10,2) NOT NULL,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE inventory (
  product_id     VARCHAR(64) PRIMARY KEY,
  stock_count    INT NOT NULL,
  reserved_count INT NOT NULL DEFAULT 0,
  version        INT NOT NULL DEFAULT 1,
  updated_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT chk_stock_non_negative CHECK (stock_count >= 0),
  CONSTRAINT fk_inventory_product FOREIGN KEY (product_id) REFERENCES products (product_id)
);

CREATE TABLE orders (
  order_id    INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  status      ENUM('pending','paid','shipped','cancelled') NOT NULL DEFAULT 'pending',
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

CREATE TABLE order_items (
  order_item_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id      INT NOT NULL,
  product_id    VARCHAR(64) NOT NULL,
  quantity      INT NOT NULL,
  unit_price    DECIMAL(10,2) NOT NULL,
  CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES orders (order_id),
  CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES products (product_id)
);

CREATE TABLE transactions (
  transaction_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  order_id       INT NOT NULL,
  customer_id    INT NOT NULL,
  amount         DECIMAL(12,2) NOT NULL,
  status         ENUM('pending','completed','failed','refunded') NOT NULL DEFAULT 'pending',
  created_at     DATETIME NOT NULL,
  KEY idx_tx_created (created_at),
  KEY idx_tx_customer (customer_id),
  KEY idx_tx_status (status),
  KEY idx_tx_keyset (created_at, transaction_id)
);

CREATE TABLE store_credit (
  customer_id INT PRIMARY KEY,
  balance     DECIMAL(10,2) NOT NULL,
  version     INT NOT NULL DEFAULT 1,
  updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE users (
  user_id    INT AUTO_INCREMENT PRIMARY KEY,
  username   VARCHAR(64) NOT NULL,
  role       VARCHAR(32) NOT NULL DEFAULT 'qa'
);

CREATE TABLE order_audit (
  audit_id   INT AUTO_INCREMENT PRIMARY KEY,
  order_id   INT NOT NULL,
  action     VARCHAR(64) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Sample data used across the test cases.
INSERT INTO customers (customer_id, name, email, status, phone_number) VALUES
  (101, 'Alice', 'alice@urbanthreads.com', 'active', '+1-555-123-4567'),
  (102, 'Bob',   'bob@urbanthreads.com',   'inactive', NULL),
  (103, 'Carol', 'carol@urbanthreads.com', 'active',   NULL);

INSERT INTO products (product_id, name, price) VALUES
  ('retro-denim-jacket', 'Retro Denim Jacket', 89.99),
  ('plain-white-tee',    'Plain White Tee',    19.99);

INSERT INTO inventory (product_id, stock_count, reserved_count) VALUES
  ('retro-denim-jacket', 10, 0),
  ('plain-white-tee',    40, 0);

INSERT INTO store_credit (customer_id, balance) VALUES
  (101, 250.00),
  (102, 75.00);
