# File Upload Test Cases — Companion

Runnable materials for the [File Upload Test Cases: Drag & Drop, Progress and UX](https://qapractices.com/test-cases/file-upload-test-cases/) resource on QAPractices.

## Contents

| File | What it is |
|---|---|
| `upload-demo/index.html` | DocDrop 2.3 widget: drop zone with hidden file input, `accept` whitelist and 10 MB limit. |
| `upload-demo/upload.js` | Queue logic: client-side type/size/empty checks before any request, per-file progress via `xhr.upload`, cancel/retry/remove controls, error states with reasons. |
| `file-upload-ui.spec.ts` | Playwright 1.48 spec with 4 tests: happy path, client-side `.exe` rejection (asserts zero POSTs), server-500 retry state, queue removal. Stubs `/api/upload` via `page.route`. |
| `package.json` | `@playwright/test` dependency and the `test` script. |

## Quick start

```bash
npm install
npx playwright install chromium
npm test
```

To poke at the widget manually, serve `upload-demo/` with any static server (e.g. `npx http-server upload-demo -p 8080`) and open `http://localhost:8080` — uploads will fail without a real `/api/upload` endpoint, which is itself a decent manual test of the error states.

## Notes

- `setInputFiles` works on the hidden input — that's the fast path. The drop-zone path needs a synthesized `DataTransfer` and only catches a broken `dragover`/`drop` handler.
- The client-side checks (extension, empty, size) run **before** `xhr.open`, so a rejection should produce zero network requests — the spec asserts exactly that.
- Server-side validation (magic bytes, AV, traversal) is intentionally out of scope; the API-level suite lives in `file-upload-download-test-cases`.
