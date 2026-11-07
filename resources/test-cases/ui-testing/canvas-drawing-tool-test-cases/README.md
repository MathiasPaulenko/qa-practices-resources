# Canvas Drawing Tool Test Cases — Runnable Companion

> Runnable examples for [Canvas Drawing Tool Test Cases](https://qapractices.com/test-cases/canvas-drawing-tool-test-cases/).

Canvas content lives in a bitmap, not in the DOM — so these examples assert against pixel data (`toDataURL`, PNG bytes) instead of selectors.

## Files

- `canvas-drawing.spec.ts` — Playwright 1.49 spec covering mouse stroke (TC-001), undo restore (TC-006), touch stroke (TC-019), and PNG export download (TC-009).
- `fixture/canvas-draw.html` — minimal drawing app with `pointerdown`/`pointermove`/`pointerup`/`pointercancel` handling, an image-data history stack, undo, and `toDataURL` PNG export.
- `canvas_export_check.py` — Pillow-based check that an exported PNG has the right dimensions and is not fully transparent.

## How to use

```bash
npm install
npx playwright install chromium
npm test

# after a run, verify a downloaded export
python canvas_export_check.py canvas.png 600 400
```

## Requirements

- Node.js 20+, Playwright 1.49
- Python 3.11+ with Pillow for the export check

## Notes

- The fixture uses Pointer Events, so `pointerType: 'touch'` dispatches work without a real device. Real pressure values still need hardware — see TC-021 in the source resource.
- `toDataURL` comparisons are exact: any anti-aliasing difference between environments can produce false positives. For looser matching, compare `getImageData` regions instead.
