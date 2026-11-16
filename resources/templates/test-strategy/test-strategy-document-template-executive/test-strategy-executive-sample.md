# Test Strategy Document — NovaBank Mobile Relaunch

> Fully completed sample of the executive test strategy template.
> Program: consumer banking app rewrite (biometric login, instant transfers,
> card controls), replacing the 2019 hybrid app.

## 1. Business Context

| Field | Value |
|---|---|
| Program | NovaBank Mobile Relaunch v2.0 (Nov 2026) |
| Sponsor | VP of Retail Banking |
| QA Lead | Tomás Herrera |
| Duration | March 2026 – January 2027 |
| Users | 1.8M account holders |
| Revenue at risk | $120M managed; churn if onboarding fails |
| Compliance | PCI DSS, PSD2 SCA, local regulator audit |

## 2. Top Risks

| Risk | Score | Response |
|---|---|---|
| Biometric auth fails on supported devices | Critical | 40-device matrix, PIN fallback |
| Instant transfer duplicates under retry | High | Idempotency testing, distributed lock |
| Migration corrupts balances | High | 2-week parallel run, daily reconcile |
| Regulator rejects PSD2 SCA flow | High | Legal review before UAT |
| App store rejection delays launch | Medium | Pre-submission checklist, 10% staged rollout |

## 3. Quality Gates

Gate 0 requirements sign-off → Gate 1 sprint exit (>95% automation pass) →
Gate 2 integration (contracts verified) → Gate 3 system test (>85% coverage) →
Gate 4 UAT (>95% scenarios) → Gate 5 release readiness (CAB decision).

## 4. Test Scope

- **In scope:** biometric + PIN login, instant transfers, card freeze/limits, balance migration, push notifications, offline read-only mode.
- **Out of scope:** web banking, ATM network, customer-support chatbot, loan origination module (phase 2).

## 5. Resources and Environments

| Item | Decision |
|---|---|
| Team | 6 QA (2 automation, 1 security, 1 performance, 2 functional) + shared SDET pool |
| Environments | dev → staging → pre-prod with prod-like data masking; device farm for biometric matrix |
| Data | synthetic dataset + masked production snapshot refreshed weekly |

## 6. Tools and Metrics

| Area | Tool / Metric |
|---|---|
| UI automation | Appium 2.x on 40-device matrix (Bitrise) |
| Contract testing | Pact 4.x against 12 services |
| Performance | k6, target p95 <500ms at 2× peak load |
| Security | OWASP ZAP weekly + external pentest pre-Gate 4 |
| KPIs | coverage, automation pass rate, defect escape rate, gate pass rate |

## 7. Release Readiness (Gate 5, filled)

| Criterion | Target | Actual | Status |
|---|---|---|---|
| Coverage | >85% | 91% | Pass |
| Automation pass | >95% | 97% | Pass |
| Open S1/S2 | 0 | 0 | Pass |
| Performance | p95 <500ms | 420ms | Pass |
| Security | No critical | 2 medium, accepted | Pass |
| Rollback | Verified | Rehearsed 2026-11-01 | Pass |

Stakeholders: weekly steering deck (one-pager), CAB sign-off at Gate 5, 10% staged rollout with instant rollback.

## 8. Compliance and Continuous Improvement

- PCI DSS 4.0 evidence collected per gate; PSD2 SCA flow reviewed by legal before UAT.
- Gate-3 defect taxonomy feeds sprint retros; escaped-defect review 30 days post-release.
