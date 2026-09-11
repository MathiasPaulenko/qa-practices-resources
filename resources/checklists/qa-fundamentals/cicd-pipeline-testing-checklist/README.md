# CI/CD Pipeline Testing Checklist — Companion

This companion provides runnable files for the [CI/CD Pipeline Testing Checklist](https://qapractices.com/checklists/cicd-pipeline-testing-checklist) checklist.

## Files

| File | Purpose |
|------|---------|
| `workflows/test-and-deploy.yml` | GitHub Actions pipeline with test and deploy stages |
| `workflows/gitlab-ci.yml` | GitLab CI config with build, SAST and deploy stages |
| `tests/test_smoke.py` | Python smoke test for post-deploy verification |

## Quick Start

```bash
# GitHub Actions: push to main to trigger the pipeline
git push origin main

# GitLab CI: push to trigger the pipeline
git push origin main

# Run smoke tests locally
pip install requests
python tests/test_smoke.py
```