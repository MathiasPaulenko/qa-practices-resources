# Security Testing Interview Questions — Examples

Payloads, proof-of-concept pages and scan configuration referenced by the
[30 Security Testing Interview Questions](https://qapractices.com/documentation/security-testing-interview-questions) guide.

> Use these payloads only on systems you own or have written permission to test.

## Contents

- `payloads/sqli.txt` — SQL injection payloads for login forms, search fields and API parameters.
- `payloads/ssrf.txt` — SSRF target candidates including localhost, AWS instance metadata and internal services.
- `payloads/mass-assignment.json` — extra-field body to test whether an API maps unfiltered input fields.
- `poc/csrf-transfer.html` — minimal CSRF proof of concept: auto-submitted form from a different origin.
- `poc/clickjacking-test.html` — iframe test page: if the target renders, framing protection is missing.
- `scripts/zap-baseline-scan.sh` — OWASP ZAP 2.14.0 baseline scan via Docker.
- `.github/workflows/security-scan.yml` — GitHub Actions job running `zaproxy/action-baseline@v0.11.0` with build failure on findings.

## Usage

```bash
# ZAP baseline scan against a staging target
./scripts/zap-baseline-scan.sh https://staging.your-app.example
```

For the full question-by-question walkthrough, read the guide on QAPractices.
