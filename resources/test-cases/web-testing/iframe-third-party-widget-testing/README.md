# iframe & Third-Party Widget Testing — Playwright companion

Companion for [iframe & Third-Party Widget Testing Test Cases](https://qapractices.com/test-cases/iframe-third-party-widget-testing/).

- `fixture-widget.html` — the "third-party widget": a page that posts messages to its parent.
- `fixture-host.html` — the host page: sandboxed iframe + `event.origin` allowlist (accepts `null` for the `file://` demo; swap in your real widget origin).
- `hostile-embed.html` — a transparent-overlay embed for the TC-04 clickjacking case.
- `iframe.spec.ts` — Playwright 1.48 specs for TC-01/07 (sandbox + title) and TC-02 (forged origin rejected, legit accepted).

## Run

```bash
npm install
npx playwright install chromium   # first time
npm test
```

To test on a real origin (and verify `X-Frame-Options`/`frame-ancestors` against TC-04), serve the folder (`npx serve .`) instead of `file://` — the hostile embed then hits actual headers.
