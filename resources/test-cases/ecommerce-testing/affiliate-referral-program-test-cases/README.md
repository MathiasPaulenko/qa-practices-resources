# Affiliate and Referral Program Test Cases — Playwright companion

Companion for [Affiliate and Referral Program Test Cases](https://qapractices.com/test-cases/affiliate-referral-program-test-cases/).

- `fixture-referral.html` — self-contained simulation of the TaskFlow referral flow: `?code=LUIS25` sets the tracking cookie, sign-up stores `referred_by`, and the purchase step runs attribution plus the self-referral fraud check. Loads via `file://`, no server needed.
- `referral-flow.spec.ts` — Playwright 1.48 spec covering TC003/TC005/TC006 (attribution + reward credited), TC009 (self-referral blocked via `luis.herrera+alias`), and the no-cookie organic path.
- `referrals-api.http` — the two curl calls from the resource (generate code, track conversion) plus the 400 case for a code over the 32-char limit. Needs a real staging API to run.

## Run

```bash
npm install
npx playwright install chromium   # first time
npm test
```

To see the fraud check fail on purpose, remove the `selfReferral` guard in the fixture — the second test then proves TC009 is catching a real bug.
