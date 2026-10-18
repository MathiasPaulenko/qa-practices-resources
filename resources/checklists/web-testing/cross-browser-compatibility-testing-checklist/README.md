# Cross-Browser Compatibility Matrix Checklist — Companion

Companion files for the [Cross-Browser Compatibility Matrix Checklist](https://qapractices.com/checklists/cross-browser-compatibility-testing-checklist) resource.

The matrices are shipped as importable CSVs so you can paste them into a spreadsheet, a test-management tool, or a tracking ticket without retyping.

## Files

| File | Contents |
|---|---|
| `browser-matrix.csv` | Target browser rows: engine, browser, version, OS/device, display scale, priority, evidence |
| `viewport-matrix.csv` | Viewport rows: name, dimensions, DPR, test focus |
| `checklist-items.csv` | All 29 checklist items across 5 areas (Environment Parity, CSS & Rendering, JavaScript & APIs, Forms & Input, Edge & Negative) with a risk level per item |

## Usage

- Import `browser-matrix.csv` and `viewport-matrix.csv` into your test plan and drop rows that are below your analytics share.
- Import `checklist-items.csv` as tasks (e.g. into Jira, TestRail or a spreadsheet) and sort by `risk` — run `High` first.
- Regenerate the browser rows from your own analytics: keep engines covering ≥ 5% of traffic as P1.

Site resource: [qapractices.com/checklists/cross-browser-compatibility-testing-checklist](https://qapractices.com/checklists/cross-browser-compatibility-testing-checklist)
