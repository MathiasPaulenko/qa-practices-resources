# Test Data Privacy Masking Document

## 1. Data Classification

| Data Category | Examples | Risk Level | Masking Required | Regulation |
|---|---|---|---|---|
| Direct identifiers | [Name, email, ID, phone] | High | Yes — always | GDPR Art. 4(1) |
| Indirect identifiers | [IP, device ID, location] | High | Yes — always | GDPR Art. 4(1) |
| Sensitive data | [Health, religion, biometrics] | Critical | Yes — always | GDPR Art. 9 |
| Financial data | [Card numbers, bank accounts] | Critical | Yes — always | PCI-DSS |
| Behavioral data | [Purchase history, clicks] | Medium | Yes — contextual | GDPR Art. 4(1) |
| Pseudonymous data | [Hashed user IDs] | Low | Contextual | GDPR Art. 4(5) |
| Anonymous data | [Aggregated statistics] | None | No | Out of scope |

## 2. Masking Techniques

| Technique | Description | Reversible | Use Case | Example |
|---|---|---|---|---|
| Substitution | Replace with fake but realistic data | No | Names, addresses | John -> Jane Smith |
| Shuffling | Swap values within the same column | No | Categorical data | Shuffle cities |
| Number variance | Add/subtract a random percentage | No | Numeric data | Salary +/- 10% |
| Masking | Partially hide data | No | Display, logs | CC: ****-****-****-1234 |
| Hashing | One-way hash function | No | Identifiers | email -> SHA-256 |
| Tokenization | Replace with token, keep mapping | Yes | Payment data | CC -> token_abc123 |
| Encryption | Encrypt with a key | Yes | Storage | AES-256 encrypt |
| Nulling | Replace with null | No | Non-essential PII | ID -> NULL |
| Generalization | Reduce precision | No | Age, location | Age 34 -> 30-40 range |

## 3. Field-by-Field Masking Rules

| Field | Technique | Format | Notes |
|---|---|---|---|
| [Field name] | [Technique] | [Format / rule] | [Constraint, e.g. keep referential integrity] |
| [Field name] | [Technique] | [Format / rule] | |

## 4. Test Data Pipeline

| Step | Action | Owner | Tool | Verification |
|---|---|---|---|---|
| 1. Export from prod | DB snapshot or API export | [Role] | [Tool] | Export log |
| 2. Classify fields | Tag PII fields | [Role] | [Tool] | Classification report |
| 3. Apply masking | Run masking rules | [Role] | [Tool] | Masking log |
| 4. Validate masking | Verify no PII remains | QA | [Script] | Validation report |
| 5. Load to test env | Import masked data | [Role] | [Tool] | Load confirmation |
| 6. Audit trail | Log all steps | [Role] | [Tool] | Audit log |
| 7. Cleanup | Purge after retention period | [Role] | [Script] | Cleanup log |

## 5. Compliance Checklist

| Requirement | Framework | Status | Evidence |
|---|---|---|---|
| No real personal data in non-prod | GDPR | [ ] | [Policy link] |
| Data minimization in test environments | GDPR | [ ] | [Notes] |
| Masking applied before data leaves prod | GDPR | [ ] | [Process doc] |
| Test environments access controlled | GDPR | [ ] | [Access policy] |
| No production credentials in test | GDPR | [ ] | [Secrets scan] |
| Data retention limits for test data | GDPR | [ ] | [Policy link] |
| DPIA completed for test data process | GDPR | [ ] | [DPIA doc] |
| Audit trail for data masking | GDPR | [ ] | [Log sample] |
| Consumer data not used in testing | CCPA | [ ] | [Notes] |
| Right to deletion applies to test copies | CCPA | [ ] | [Process] |

## 6. Validation Tests

| Test ID | Scenario | Expected | Pass |
|---|---|---|---|
| TD-001 | No real emails in test DB | All emails end in @example.test | [ ] |
| TD-002 | No real IDs in test DB | All IDs masked or null | [ ] |
| TD-003 | No real credit card numbers | All cards tokenized | [ ] |
| TD-004 | No real phone numbers | All phones use 555 prefix | [ ] |
| TD-005 | No real IP addresses | All IPs in private range | [ ] |
| TD-006 | Referential integrity preserved | Foreign keys still valid | [ ] |
| TD-007 | Data format preserved | Masked data matches original format | [ ] |
| TD-008 | No PII in logs | Log scan finds no PII | [ ] |

## 7. Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| **QA Lead** | [Name] | [YYYY-MM-DD] | [Masking verified] |
| **Data Protection Officer** | [Name] | [YYYY-MM-DD] | [Compliance confirmed] |
| **Engineering Manager** | [Name] | [YYYY-MM-DD] | [Approved for use] |
