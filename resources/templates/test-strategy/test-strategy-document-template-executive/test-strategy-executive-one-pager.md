# Test Strategy — One-Pager

> Condensed version for quick steering-committee sign-off.
> Same decisions, 10% of the pages.

## Program

**[Program name]** — [one line: what it is, when it ships]
Sponsor: [name] · QA Lead: [name] · Release: [version + date]

## Why we test this way

| Top 3 risks | Score | Response |
|---|---|---|
| [risk 1] | [Critical/High/Med] | [one-line response] |
| [risk 2] | [score] | [response] |
| [risk 3] | [score] | [response] |

## The gates

Requirements → Sprint → Integration → System → UAT → **Release**
Each gate: one authority, one criterion, one answer (pass/fail + who can waive).

## Readiness snapshot

| Criterion | Target | Actual | Status |
|---|---|---|---|
| Coverage | >85% | [ ] | [ ] |
| Open S1/S2 | 0 | [ ] | [ ] |
| Performance | p95 <[x]ms | [ ] | [ ] |
| Security | no critical | [ ] | [ ] |
| Rollback | verified | [ ] | [ ] |

## Decision requested

**Release / hold** — signed by [sponsor] on [date].
