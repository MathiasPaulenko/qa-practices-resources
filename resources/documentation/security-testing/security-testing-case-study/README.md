# Security Testing Case Study: SecureBank — Pipeline Configs

Companion files for the [Security Testing Case Study: SecureBank](https://qapractices.com/documentation/security-testing-case-study/) article ([versión en español](https://qapractices.com/es/documentation/security-testing-case-study/)).

These are the configs SecureBank wired into GitHub Actions over 16 weeks: SAST + SCA gates on every pull request, authenticated DAST nightly against staging, and secret scanning on every commit — all feeding one findings tracker with severity, owner, and SLA.

## What's included

| File | What it does |
| --- | --- |
| `security-gates.yml` | GitHub Actions workflow: Semgrep 1.184 + Snyk + SonarQube on PRs, OWASP ZAP full scan nightly. Copy to `.github/workflows/` |
| `pre-commit-config.yaml` | GitLeaks 8.28 pre-commit hook. Copy to `.pre-commit-config.yaml` |
| `zap/securebank.context` | ZAP scan context template with JSON auth + bearer token session — what makes the scan authenticated |
| `zap/rules.tsv` | Alert filtering rules for `action-full-scan` (downgrades known noise, keeps real signal) |
| `findings-tracker.sample.json` | Findings tracker schema with `dedupKey`, severity SLAs (24h / 7d / 30d) and sample records |

## How to use

1. **Pre-commit (fastest win, ~1 hour):** copy `pre-commit-config.yaml` to `.pre-commit-config.yaml`, then `pipx install pre-commit && pre-commit install`.
2. **PR gates:** copy `security-gates.yml` to `.github/workflows/`. Set repo secrets `SEMGREP_APP_TOKEN`, `SNYK_TOKEN`, `SONAR_TOKEN`, `SONAR_HOST_URL`.
3. **Nightly DAST:** point `target` at your staging URL. Export a real context from ZAP Desktop (Session → Context → Export) after recording a login, and use `zap/securebank.context` as the reference template. Tune `zap/rules.tsv` to your stack.
4. **Tracker:** adapt `findings-tracker.sample.json` to whatever tracker you use — the key fields are `severity`, `owner`, `slaHours`, and `dedupKey`.

## Prerequisites

- GitHub Actions runners (ubuntu-latest) or equivalent CI
- `pre-commit` + `pipx` for local hooks
- OWASP ZAP context file exported from ZAP Desktop for authenticated scanning
- Snyk and Semgrep AppSec Platform accounts for the SCA/SAST jobs

## Notes

- `staging.securebank.internal` is the fictional target from the case study — replace it.
- Authenticated DAST is the difference between ~20% and ~80% coverage; unauthenticated scans can't see access-control issues.
- Tune SAST rules before enabling blocking gates, or the first week floods developers with false positives.
