# Password Security Testing Examples

Runnable snippets used in the QAPractices guide:

- [Password Security Testing Guide](https://qapractices.com/documentation/password-security/)

Three pieces, each matching a section of the guide:

| File | What it tests |
|---|---|
| `breach_check.py` | Have I Been Pwned k-anonymity lookup — rejects passwords found in breach corpora without sending the password anywhere |
| `password_policy.js` | NIST 800-63B-style policy: minimum length 12 + blocklist, no composition rules |
| `login_rate_limit.spec.ts` | Playwright spec: lockout after 5 failed attempts + generic error that does not reveal account existence |

## Run

```bash
# Python 3.11+ — breach check (hits the live HIBP API)
pip install -r requirements.txt
python breach_check.py "Correct-Horse-Battery-Staple!"

# Node 20+ — policy self-check, no dependencies
node password_policy.js

# Playwright — rate-limit spec against your staging env
npm install
npx playwright install chromium
BASE_URL=https://staging.example.dev npx playwright test
```

The Playwright spec needs a real login page — point `BASE_URL` at staging and
adjust the selectors and expected lockout text to your app.
