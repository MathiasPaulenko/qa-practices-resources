# Example Output — Generated Entity Plan (fragment)

What the generated strategy looks like for the e-commerce input above.

| Entity | Fields | Volume | Key Constraints |
|---|---|---|---|
| Customers | id, name, email, phone, address, tier | 100,000 | Unique emails, valid postal codes per country |
| Products | id, sku, name, category, price, stock | 10,000 | Unique SKU, positive price, stock >= 0 |
| Orders | id, customer_id, status, total, created_at | 500,000 | FK to customers, status enum, total > 0 |
| OrderItems | id, order_id, product_id, qty, price | 2,000,000 | FK to orders and products, qty > 0 |
| Reviews | id, product_id, customer_id, rating, text | 50,000 | Rating 1-5, FK constraints, text length 10-2000 |

The full deliverable also includes: generation script skeleton (Faker + seeds), SQL DDL with constraints and indexes, a 10-record sample per entity, a volume benchmark, and validation queries.
