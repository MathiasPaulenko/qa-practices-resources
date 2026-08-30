# Ecommerce Testing Checklist

> Printable companion for [Ecommerce Testing Checklist](https://qapractices.com/checklists/ecommerce-testing-checklist).

This repository contains a printable/importable version of the ecommerce testing checklist from QAPractices.

## Files

- `ecommerce-testing-checklist.md` — Markdown version, ready to print or paste into a test management tool.
- `ecommerce-testing-checklist.json` — Structured JSON version with risk levels and categories, suitable for importing into Jira, TestRail, Notion or a custom test runner.

## How to use

1. Open `ecommerce-testing-checklist.md` before a release cycle.
2. Mark each item `[x]` as you validate it.
3. Sort by **Risk: High** first when time is short.
4. Import `ecommerce-testing-checklist.json` into your test management tool if you want tracked test cases.

## Risk levels

- **High** — Security, payment, inventory, PII or core checkout flow. A failure directly costs revenue or creates compliance issues.
- **Medium** — Important functionality or regression risk. A failure is visible but usually recoverable.
- **Low** — Nice-to-have, accessibility, performance or SEO improvements.

## Categories

- Product Catalog
- Shopping Cart
- Checkout
- Payment
- Order & Inventory
- Security & Compliance
- Performance & Mobile
- Notifications & SEO
- Accessibility
- Edge Cases & Negative Checks
