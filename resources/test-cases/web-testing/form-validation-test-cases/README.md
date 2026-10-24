# Form Validation Test Cases Companion

Runnable examples for the [Form Validation Test Cases](https://qapractices.com/test-cases/form-validation-test-cases/) resource on QAPractices. It maps to the Automation Examples section: a demo HTML5 form, a shared Zod schema used on both client and server sides, and a Playwright suite covering client-side checks, server parity and file-upload spoofing.

## Contents

| File | Purpose |
|---|---|
| `demo-form.html` | Self-contained registration form with HTML5 constraints, `aria-*` wiring and a magic-byte PDF check |
| `schema.js` | Zod 3.23 registration schema shared by client and server validation |
| `form-validation.spec.ts` | Playwright 1.49 suite: required fields, whitespace, error clearing, schema parity, renamed-`.exe` rejection |
| `fixtures/payload.exe` | Executable fixture (real `MZ` header) for the extension-spoofing case TC-FV-080 |

## Run

```bash
npm install
npx playwright install chromium
npx serve . -l 4173   # static server for demo-form.html
npm test
```

The schema checks run inside the Playwright suite — no separate runner needed.

## Notes

- The demo form uses `novalidate` and JS checks so the same rules can be replayed server-side; in production, drive both from the shared schema.
- `fixtures/payload.exe` contains only the `MZ` signature followed by padding — it is inert, but treat it as hostile input by design.
