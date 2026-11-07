# Best Security Testing Tools — Runnable Scan Examples

Runnable versions of the three examples from the article
[Best Security Testing Tools (2026): Vulnerability Scanning](https://qapractices.com/documentation/best-security-testing-tools/).

## Contents

| File | What it does |
|---|---|
| `zap-baseline.sh` | OWASP ZAP baseline scan against a running app via Docker (`ghcr.io/zaproxy/zaproxy:stable`, ZAP 2.15 line). Writes `zap-baseline.html`. |
| `nuclei-scan.sh` | Targeted Nuclei v3 scan: critical/high severity templates, rate-limited to 10 req/s. |
| `github-actions/dependency-check.yml` | GitHub Actions job running OWASP Dependency-Check against the NVD feed on every push; fails on CVSS ≥ 7 and uploads the HTML report. |

## Usage

```bash
./zap-baseline.sh https://staging.example.com
./nuclei-scan.sh https://staging.example.com
```

For the GitHub Actions job, copy `github-actions/dependency-check.yml` into
`.github/workflows/` in your repository. The scan needs a `NVD_API_KEY` for
reliable feed downloads on busy runners — request one at
<https://nvd.nist.gov/developers/request-an-api-key> and add it as a step
environment variable if throttling appears.

## Requirements

- Docker (for the ZAP baseline script)
- Nuclei v3 — `go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest`
- A GitHub repository with Actions enabled (for the workflow file)

## Choosing a tool

These scripts cover the three highest-ROI layers from the article:
dependency scanning (Dependency-Check), runtime DAST (ZAP baseline), and
targeted template scanning (Nuclei). They complement each other — none of
them replaces manual penetration testing before major releases.
