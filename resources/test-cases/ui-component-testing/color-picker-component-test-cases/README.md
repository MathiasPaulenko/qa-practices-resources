# Color Picker Component Test Cases — runnable examples

Companion for [Color Picker Component Test Cases: Select, Preview, Input](https://qapractices.com/test-cases/color-picker-component-test-cases/).

## Contents

- `color-utils.js` — WCAG 2.x relative luminance + contrast ratio, hex parsing and validation.
- `color-utils.test.mjs` — Node test-runner checks (`node --test`), no dependencies.
- `color-picker.spec.ts` — Playwright 1.48 spec: hex input, invalid hex, clipboard, axe-core 4.10 scan.

## Run

```bash
npm install
npm test            # unit: contrast + hex parsing
npm run test:e2e    # needs an app exposing /editor/palette with the data-testid hooks
```

The spec targets a picker exposing `data-testid` hooks (`color-picker-trigger`, `hex-input`, `color-preview`, `copy-color`, `hex-error`). Adapt the selectors to your implementation.
