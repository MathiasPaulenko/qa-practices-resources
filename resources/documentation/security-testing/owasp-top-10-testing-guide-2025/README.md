# OWASP Top 10 Testing Guide 2025 — Companion

> Companion repository for [10 OWASP Top 10 Testing Scenarios for LumaPay 2025](https://qapractices.com/documentation/owasp-top-10-testing-guide-2025/)

## Requirements

- Python 3.10+
- GitHub Actions
- A staging environment with HMAC-signed logs

## Files

| File | Purpose |
| --- | --- |
| `security.yml` | GitHub Actions workflow with SAST, dependency scan and container scan gates |
| `log_integrity_check.py` | HMAC signature verification script for A09 logging tests |
| `meta.json` | Resource metadata |
| `sample-log.txt` | Sample log file with HMAC signatures for testing the script |

## Usage

### Log integrity check (A09)

```bash
# Set the HMAC secret (use the same secret your app uses to sign logs)
export LOG_HMAC_SECRET="your-secret-key"

# Run the check
python log_integrity_check.py evidence/batch327/a09-login.log
```

Output:

```text
Log integrity check for: evidence/batch327/a09-login.log
  Total lines: 150
  Verified:     150
  Failed:       0

  RESULT: PASS — all lines verified
```

### GitHub Actions workflow

Copy `security.yml` to `.github/workflows/security.yml` in your repository. The workflow runs:

- SAST with SonarQube 10.6
- Dependency scan with npm audit
- Container scan with Trivy 0.57.1

## License

MIT — Mathias Paulenko
