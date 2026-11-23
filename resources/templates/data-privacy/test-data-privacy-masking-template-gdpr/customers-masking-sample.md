# Test Data Privacy Masking Document — Northline Commerce (Completed Sample)

Scope: `customers` table export for the staging refresh of 2026-11-14. 41,208 rows, PostgreSQL 16.

## 1. Field-by-Field Masking Rules (applied)

| Field | Technique | Before | After |
|---|---|---|---|
| first_name | Substitution | `Margaret` | `Olivia` |
| last_name | Substitution | `Chen` | `Almeida` |
| email | Substitution | `m.chen@realmail.com` | `m.chen@example.test` |
| phone | Substitution | `+1-415-555-0192` | `+1-555-0144-2271` |
| ssn | Nulling | `523-41-8890` | `NULL` |
| card_number | Tokenization | `4111-...-1111` | `tok_x7f2a91` |
| last_login_ip | Substitution | `84.17.32.9` | `10.14.6.77` |
| date_of_birth | Generalization | `1988-03-14` | `1985-1990` |

## 2. Pipeline Run

| Step | Result | Verified by |
|---|---|---|
| 1. Export | 41,208 rows, `customers_prod_20261114.dump` | DBA log |
| 2. Classification | 8 PII fields tagged | Classification report |
| 3. Masking | Completed in 4 min, all rules applied | Masking log |
| 4. Validation | TD-001 to TD-008 pass; 0 suspicious rows | `masking-validation.sql` |
| 5. Load | Staging `customers` refreshed | DevOps log |
| 6. Audit trail | All steps logged | Audit log |
| 7. Cleanup | Retention set to 2026-12-14 | Scheduled purge |

## 3. Validation Results

| Test ID | Scenario | Result | Pass |
|---|---|---|---|
| TD-001 | No real emails in test DB | 0 rows outside @example.test | [x] |
| TD-002 | No real IDs in test DB | All NULL or masked | [x] |
| TD-003 | No real credit card numbers | All tok_% tokens | [x] |
| TD-004 | No real phone numbers | All 555 prefix | [x] |
| TD-005 | No real IP addresses | All private range | [x] |
| TD-006 | Referential integrity preserved | 0 orphan orders | [x] |
| TD-007 | Data format preserved | 0 malformed emails | [x] |
| TD-008 | No PII in logs | Log scan clean | [x] |

## 4. Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| **QA Lead** | Priya Nair | 2026-11-14 | Masking verified |
| **Data Protection Officer** | Tomás Herrera | 2026-11-15 | Compliance confirmed |
| **Engineering Manager** | Julia Brandt | 2026-11-15 | Approved for use |
