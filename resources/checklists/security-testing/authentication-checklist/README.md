# Authentication Testing Checklist — Companion

This companion provides runnable files for the [Authentication Testing Checklist](https://qapractices.com/checklists/authentication-checklist) checklist.

## Files

| File | Purpose |
|------|---------|
| `src/brute-force-lockout-test.ts` | Playwright test for account lockout after repeated failed logins |
| `src/security-header-validation.py` | Python script to validate security headers on login endpoint |
| `src/jwt-expiration-test.py` | Python script to test JWT token expiration and validation |

## Quick Start

```bash
# Install Playwright
npm init -y && npm install @playwright/test

# Run the brute force lockout test
npx playwright test src/brute-force-lockout-test.ts

# Run the security header validation
pip install requests
python src/security-header-validation.py

# Run the JWT expiration test
pip install pyjwt
python src/jwt-expiration-test.py
```