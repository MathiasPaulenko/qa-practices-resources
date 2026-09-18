# Accessibility Testing with axe-core — Runnable Examples

Companion repository for the QAPractices guide
[How to Perform Accessibility Testing with axe-core](https://qapractices.com/documentation/accessibility-testing-axe-core/)
([versión en español](https://qapractices.com/es/documentation/accessibility-testing-axe-core/)).

All examples are self-contained: the Playwright suite renders inline HTML fixtures
with `page.setContent()` and the Jest suite tests markup strings — no external
site or backend is required. The Python suite needs a local Chrome install.

## Layout

```text
playwright/   @axe-core/playwright 4.13.0 + @playwright/test 1.63.0
jest/         jest-axe 11.0.0 + jest 30.5.1
python/       axe-selenium-python 3.0.0 + selenium 4 (needs local Chrome)
```

## Playwright

```bash
cd playwright
npm install
npx playwright test
```

The config uses `channel: 'chrome'` — it runs your installed Chrome, so no
browser download is needed. For CI, remove the channel option and run
`npx playwright install chromium` to use the bundled browser.

Four tests cover: a clean page passing, a fixture with intentional violations
(`image-alt`, `color-contrast`, missing label, missing `lang`), impact-based
gating (`critical`/`serious`), and a scoped `.include()` scan. Note the tag
filter detail: `image-alt` is a Level A rule — a `wcag2aa`-only tag set filters
it out, so include `wcag2a` when you want full coverage.

## Jest (component level)

```bash
cd jest
npm install
npm test
```

jest-axe checks rendered markup without a browser — fast first pass for
components. It cannot see layout, focus order or anything the browser computes:
the `color-contrast` rule silently returns no findings under jsdom, so contrast
must be verified with a real browser runner like `@axe-core/playwright`.

## Python (Selenium)

```bash
cd python
pip install -r requirements.txt
pytest -v
```

Requires Chrome/Chromium on the machine; Selenium 4 resolves the driver
automatically. Fixtures are injected via `data:text/html` URLs.

## Verified versions

| Package | Version |
|---|---|
| axe-core | 4.13.0 |
| @axe-core/playwright | 4.13.0 |
| @axe-core/webdriverjs | 4.13.0 |
| @playwright/test | 1.63.0 |
| jest-axe | 11.0.0 |
| jest | 30.5.1 |
| cypress-axe | 1.7.0 |
| axe-html-reporter | 2.2.11 |
| axe-selenium-java | 4.10.1 (Maven) |
| axe-selenium-python | 3.0.0 (PyPI) |

Note: `@axe-core/cypress` and `@axe-core/selenium` do **not** exist on npm —
the Cypress integration is `cypress-axe`, and Selenium users need
`@axe-core/webdriverjs` (JS) or `axe-selenium-java` (Java/Maven).
