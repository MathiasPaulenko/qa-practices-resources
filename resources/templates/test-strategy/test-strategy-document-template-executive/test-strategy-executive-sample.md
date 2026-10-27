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

## 4. Readiness Snapshot (Gate 5, filled)

| Criterion | Target | Actual | Status |
|---|---|---|---|
| Coverage | >85% | 91% | Pass |
| Automation pass | >95% | 97% | Pass |
| Open S1/S2 | 0 | 0 | Pass |
| Performance | p95 <500ms | 420ms | Pass |
| Security | No critical | 2 medium, accepted | Pass |
| Rollback | Verified | Rehearsed 2026-11-01 | Pass |
