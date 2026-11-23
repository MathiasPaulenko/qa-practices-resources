# Test Data Privacy Masking Template (GDPR) — Companion

Downloadable files for the [Test Data Privacy Masking Template](https://qapractices.com/templates/test-data-privacy-masking-template-gdpr/) on QAPractices.

## Contents

| File | Purpose |
|---|---|
| `test-data-privacy-masking-template.md` | Blank 7-section document: classification, techniques, per-field rules, pipeline, compliance checklist, validation tests and sign-off. |
| `customers-masking-sample.md` | The document filled for Northline Commerce: `customers` table (41,208 rows) masked for the staging refresh, all validation tests passing. |
| `masking-validation.sql` | PostgreSQL validation gate covering TD-001 to TD-007 — every query must return 0 before the load proceeds. |

## Usage

1. Copy `test-data-privacy-masking-template.md` into your project docs or wiki and fill sections 1-4 before the first export — never after.
2. Adapt the per-field rules to your schema; keep referential integrity in mind for keys shared across tables.
3. Wire `masking-validation.sql` into the pipeline as a hard gate: run it after masking, abort the load on any non-zero count.
4. Use `customers-masking-sample.md` as the reference for what a properly documented masking run looks like.

The SQL targets PostgreSQL; adapt the regex operators (`~`, `!~`) for MySQL or SQL Server.
