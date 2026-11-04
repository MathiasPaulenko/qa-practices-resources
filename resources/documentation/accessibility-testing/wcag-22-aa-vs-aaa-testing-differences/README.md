# WCAG 2.2 AA vs AAA Testing — Runnable Examples

Companion repository for the QAPractices guide
[WCAG 2.2 AA vs AAA Testing Differences](https://qapractices.com/documentation/wcag-22-aa-vs-aaa-testing-differences/)
([versión en español](https://qapractices.com/es/documentation/wcag-22-aa-vs-aaa-testing-differences/)).

The examples scan the same page at both conformance levels so you can measure
the real delta between an AA gate and an AAA sweep.

## Layout

```text
playwright/   @axe-core/playwright 4.14.0 + @playwright/test 1.63.0
pa11y/        pa11y 10.0.0 shell script (WCAG2AA vs WCAG2AAA)
```

## Playwright — rule-tag split

```bash
cd playwright
npm install
BASE_URL=https://staging.qapractices.com npx playwright test
```

The config uses `channel: 'chrome'` — it runs your installed Chrome, so no
browser download is needed. For CI, remove the channel option and run
`npx playwright install chromium` to use the bundled browser.

Three specs cover: the AA release gate (`wcag22aa` tag, hard fail on
violations), the AAA sweep (`wcag2aaa` tag, report-only) and a focused
`color-contrast-enhanced` pass — the rule that turns a 4.5:1 requirement into
7:1 and produces most first-scan noise.

## pa11y — both standards in one run

```bash
BASE_URL=https://staging.qapractices.com ./pa11y/run-audit.sh /checkout
```

Writes `aa-report.json` and `aaa-report.json`, then prints the issue count per
level and the number of AAA-only rule codes hit. Run it before and after a
contrast-token fix to see the enhanced-contrast findings drop.

## Notes

- axe rule tags are not conformance: an empty `wcag2aaa` scan is evidence for
  part of a claim, not proof of AAA. Reading level (3.1.5), pronunciation
  (3.1.6), context-sensitive help (3.3.5) and sign language (1.2.6) all need
  human review.
- Keep the AAA pass non-blocking until the first triage is done — enhanced
  contrast alone floods a fresh scan.
