# Image Cropping and Resizing Test Cases — Companion Lab

Companion to the [Image Cropping and Resizing Test Cases](https://qapractices.com/test-cases/image-cropping-resizing-test-cases/) resource on QAPractices.com.

`image_pipeline.py` is a Pillow-based model of the crop/resize pipeline: format sniffing, EXIF orientation normalization, bounds/min-size/aspect-ratio clamping, preview-to-source coordinate mapping under zoom, alpha-aware export, animated GIF frame cropping and batch resize. It encodes the *rules* so the failure points in the resource can be asserted without a browser — the UI-level checks use Playwright, as shown in `crop-preset.spec.ts` and the resource itself.

## What the model covers

- **Selection stage (TC-01–TC-12, TC-30):** crop drift, 1:1 and 16:9 ratio locks, free crop, min-size enforcement, bounds clamping, zoom coordinate mapping.
- **Load stage (TC-13, TC-14 + edge table):** unsupported formats, corrupted files, magic-byte sniffing, EXIF Orientation applied on decode.
- **Transform stage (TC-09, TC-15, TC-16, TC-17):** exact-dimension resize, 1×1 output, oversized bitmap cap, portrait photos staying upright.
- **Export stage (TC-10, TC-23, TC-24, TC-26, TC-27):** JPEG conversion, PNG alpha preservation, all-frames GIF cropping, quality-vs-size monotonicity, batch resize with per-file results.

## Run

```bash
pip install -r requirements.txt
pytest -v
```

Expected: `20 passed` in under a second. Tests generate their own fixtures (a portrait JPEG with `Orientation=6`, an RGBA PNG, a 12-frame GIF, a truncated JPEG, a BMP), so nothing external is needed.

## Files

- `image_pipeline.py` — `load_image`, `clamp_crop_box`, `preview_to_source`, `crop_image`, `resize_image`, `export_image`, `crop_animation`, `batch_resize`.
- `tests/test_image_pipeline.py` — 20 tests grouped by pipeline stage, named after the resource's TC ids.
- `crop-preset.spec.ts` — Playwright spec for the preset-crop browser flow (needs your app's crop UI running).
- `crop.feature` — Gherkin feature covering the end-to-end crop journey.
- `requirements.txt`, `pytest.ini` — Pillow 11.2.1 + pytest 8.3.4 pinned.
