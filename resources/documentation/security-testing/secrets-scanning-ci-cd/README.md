# Secrets Scanning in CI/CD — Companion Resources

Runnable configs from the [Secrets Scanning in CI/CD](https://qapractices.com/documentation/secrets-scanning-ci-cd/) guide on QAPractices.

## What's inside

| Path | What it is |
|---|---|
| `.pre-commit-config.yaml` | GitLeaks 8.30 pre-commit hook — blocks secrets before they enter Git history |
| `.github/workflows/secrets.yml` | GitLeaks scan on every PR and push, with `fetch-depth: 0` for full history |
| `.github/workflows/secret-scanning-pipeline.yml` | TruffleHog verified-results scan + Trivy image secret scan, fail on finding |
| `scripts/check-unmasked-secrets.sh` | Grep check for unmasked credentials printed into pipeline logs |

## Quick start

```bash
# 1. Local gate: copy the pre-commit config to your repo root
cp .pre-commit-config.yaml /path/to/your/repo/
pip install pre-commit
pre-commit install

# 2. CI gates: copy the workflows
cp .github/workflows/*.yml /path/to/your/repo/.github/workflows/

# 3. Ad-hoc scans
gitleaks detect --source . --verbose \
  --report-format json --report-path gitleaks-report.json
trufflehog git file://. --results=verified,unknown --json > trufflehog-report.json
trivy image app:scan --scanners secret --exit-code 1
```

## Rules of the house

- `GITLEAKS_LICENSE` is only required for organization accounts on `gitleaks-action`; personal repos can drop that env line.
- `fetch-depth: 0` is non-negotiable for history scans — a shallow clone scans nothing that matters.
- TruffleHog runs with `--results=verified,unknown` so live credentials surface first; review `unknown` findings manually before dismissing.
- Rotate first, debate history rewriting later. A removed secret that was already pushed is still a leaked secret.
- Document every suppression with a reason and a revisit date.

Guide: <https://qapractices.com/documentation/secrets-scanning-ci-cd/>
