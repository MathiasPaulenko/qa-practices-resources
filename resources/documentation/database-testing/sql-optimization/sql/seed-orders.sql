-- ParcelHub orders table + seed. PostgreSQL 18.
-- 1M rows keeps it quick; raise the bound to 40000000 for production scale.
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id     integer NOT NULL,
    status          text NOT NULL,
    total           numeric(10,2) NOT NULL,
    tracking_number text,
    created_at      timestamptz NOT NULL DEFAULT now()
);

INSERT INTO orders (customer_id, status, total, tracking_number, created_at)
SELECT
    (random() * 50000)::int + 1,
    (ARRAY['pending','paid','packed','shipped','delivered','returned','cancelled','refunded'])[floor(random()*8)+1],
    round((random() * 900 + 10)::numeric, 2),
    'TRK' || lpad((random()*99999999)::int::text, 8, '0'),
    now() - (random() * interval '730 days')
FROM generate_series(1, 1000000);

ANALYZE orders;

-- Enable pg_stat_statements for query ranking (needs shared_preload_libraries in production)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
