# Registration Test Cases — Companion

Runnable subset of the [Registration Test Cases](https://qapractices.com/test-cases/registration-test-cases/) — the ones worth automating first.

## Files

| File | What it does |
|---|---|
| `registration.spec.ts` | Playwright spec covering TC-008 (valid signup), TC-013 (duplicate email), TC-014 (invalid format), TC-010 (weak password) and TC-012 (unchecked terms). |
| `registration-data.json` | Test-data fixture: valid/duplicate/invalid emails plus the SQLi, XSS, unicode and tempmail payloads used in the security and edge blocks. |

## Run

```bash
BASE_URL=http://localhost:3000 npx playwright test registration.spec.ts
```

Point `BASE_URL` at staging — never production. Adjust selectors to your form's markup.

## What it demonstrates

- **The tool column is deliberate** — these five are the cases Playwright actually owns; the security probes belong to ZAP/Burp and the boundary cases to pytest parametrize.
- **Errors must be generic** — TC-013's assertion is the same message an attacker would see during enumeration (TC-022).
