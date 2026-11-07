# Accessibility Testing Tools — Runnable Examples

Companion code for [Accessibility Testing Tools: WAVE, Lighthouse, and axe-core](https://qapractices.com/documentation/accessibility-testing-tools/) on QAPractices.

Three runnable pieces covering the automated side of the guide — the manual side (NVDA, keyboard passes, contrast sampling) is covered step by step in the article itself.

## What's inside

| Path | What it does |
|---|---|
| `playwright/` | `@axe-core/playwright` 4.10 spec: full-page scan, scoped scan (include/exclude/widgets), WCAG tag filtering, single-rule contrast check |
| `ci/fail-build-if-a11y-fails.js` | CI gate that filters axe violations by `impact` (critical/serious block, moderate/minor warn) |
| `ci/lighthouserc.json` | Lighthouse CI 0.14 config: accessibility-only assertions with score >= 90 |
| `python/wave_api_check.py` | WAVE API call that prints error/contrast/alert counts for a URL |

## Quick start

```bash
# Playwright + axe-core
cd playwright && npm install && npx playwright install chromium
npx playwright test

# CI gate (run inside your axe harness)
node ci/fail-build-if-a11y-fails.js < axe-results.json

# Lighthouse accessibility-only audit
npm install -g @lhci/cli@0.14.x
lhci autorun --config=ci/lighthouserc.json

# WAVE API (needs a key from wave.webaim.org)
pip install -r python/requirements.txt
WAVE_API_KEY=your-key python python/wave_api_check.py https://staging.yourstore.com
```

## Notes

- The Playwright spec expects a local dev server or staging URL — point `BASE_URL` at yours.
- `your-wave-api-key` is a placeholder: get a real one at [wave.webaim.org/api](https://wave.webaim.org/api/).
- For the deep axe-core toolchain (Jest, Selenium/Python, intentionally-broken fixtures), see the sibling [accessibility-testing-axe-core](../accessibility-testing-axe-core/) companion.
