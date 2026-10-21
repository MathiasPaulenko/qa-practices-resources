# Cookie Consent Banner Testing — Companion

Companion resource for [Cookie Consent Banner Test Cases: 12 GDPR Scenarios](https://qapractices.com/test-cases/cookie-consent-banner-testing-test-cases/).

## Contents

- `consent-gate.mjs` — dependency-free CMP consent-gate model: vendors register per category (`necessary`/`analytics`/`marketing`), the gate fires or blocks each vendor based on the stored consent, the policy version, and the vendor's `addedIn` scope (a vendor added after consent doesn't inherit it). Includes serialization for session persistence and a GPC auto-reject default.
- `tests/consent-gate.test.mjs` — executable subset of the article's cases: banner on first visit (TC-01), granular categories (TC-02), blocking before consent (TC-03), firing after consent (TC-04), persistence via serialize/restore (TC-05), withdrawal (TC-06), GPC auto-reject (TC-10), version-bump re-prompt (TC-11), new-vendor scope (TC-12), plus corrupted-consent and uncategorized-vendor edges.

## Requirements

- Node.js 20+ (uses the built-in `node:test` runner — no npm install needed)

## Usage

```bash
node --test tests/*.test.mjs
```

Expected output: `11 passed`.

In a real CMP the same checks run as Playwright tests against the network layer (see the article's rewritten Playwright snippet) — here they're unit tests so the consent semantics stay verifiable without a browser.

## Related

- Article EN: https://qapractices.com/test-cases/cookie-consent-banner-testing-test-cases/
- Article ES: https://qapractices.com/es/test-cases/cookie-consent-banner-testing-test-cases/
