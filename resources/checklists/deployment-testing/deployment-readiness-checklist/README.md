# Deployment Readiness Checklist — Companion Scripts

> Companion repository for the [Deployment Readiness Checklist: Go-Live](https://qapractices.com/checklists/deployment-readiness-checklist) on QAPractices.com.

## What's inside

- **Verification scripts** for deployment readiness gates
- **Bash and Python** scripts for env vars, smoke tests, and canary traffic

## Scripts

| Script | Language | Purpose |
| --- | --- | --- |
| `scripts/check-env-vars.sh` | Bash | Verify all required environment variables are set before deploy |
| `scripts/post-deploy-smoke-test.py` | Python | Health endpoint and version check after deploy |
| `scripts/check-canary-traffic.sh` | Bash | Verify canary traffic is within expected range (1-10%) |

## Requirements

| Tool | Version |
| --- | --- |
| Bash | 5.0+ |
| Python | 3.10+ |
| requests | 2.31+ |
| jq | 1.6+ |
| curl | any |

## Usage

```bash
# Check environment variables
chmod +x scripts/check-env-vars.sh
./scripts/check-env-vars.sh

# Post-deploy smoke test
pip install requests
python scripts/post-deploy-smoke-test.py

# Canary traffic verification
chmod +x scripts/check-canary-traffic.sh
./scripts/check-canary-traffic.sh
```

## Related resources

- [Deployment Readiness Checklist](https://qapractices.com/checklists/deployment-readiness-checklist)
- [Release Testing Checklist](https://qapractices.com/checklists/release-testing-checklist)
- [Zero-Downtime Deployment Checklist](https://qapractices.com/checklists/zero-downtime-deployment-checklist)
- [Post-Deployment Verification Checklist](https://qapractices.com/checklists/post-deployment-verification-checklist)

## License

MIT
