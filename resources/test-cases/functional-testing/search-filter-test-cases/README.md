# Search & Filter Test Cases — Playwright Companion

Companion code for [Search and Filter Test Cases: Query Validation and UX](https://qapractices.com/test-cases/search-filter-test-cases/) on QAPractices.

## What is inside

| File | What it shows |
|------|---------------|
| `search-demo.html` | Self-contained demo page: 7-product catalog, search input with 300ms debounce, OR-within-facet / AND-across-facet logic, URL state sync, empty state, clear-all. No server needed — `file://` works. |
| `tests/search-filter.spec.ts` | 8 Playwright 1.48 specs covering TC-01, TC-07, TC-08, TC-09, TC-11, TC-13, TC-15, TC-16. |
| `package.json` | `@playwright/test` pinned at 1.48.2. |

## Run it

```bash
npm install
npx playwright install chromium   # browsers, one-time
npm test
```

All specs run against the local `search-demo.html` — no backend, no network. The debounce spec (TC-11) counts calls through the visible `#call-count` counter; the URL-state spec (TC-15) reopens the URL in a fresh page and diffs result sets.

## Related resource

- [Search and Filter Test Cases: Query Validation and UX](https://qapractices.com/test-cases/search-filter-test-cases/) — the full 16-case suite plus edge/boundary table this code automates.
