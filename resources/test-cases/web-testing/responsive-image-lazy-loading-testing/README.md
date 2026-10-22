# Responsive Image & Lazy Loading Testing — Runnable Companion

The executable pieces behind the [Responsive Image Test Cases](https://qapractices.com/test-cases/responsive-image-lazy-loading-testing/) page on QAPractices: a `picture.html` fixture exercising srcset/`sizes`, `<picture>` art direction, eager/lazy loading and a broken-image case — plus a Playwright spec and a pytest suite that verifies the fixture's markup contracts.

## Contents

| File | What it is |
|---|---|
| `picture.html` | Zero-dependency fixture: srcset hero (eager, `fetchpriority="high"`, preloaded), `<picture>` art-direction block, intentionally broken image, and a lazy image ~2000px below the fold. |
| `img/` | SVG variants (`hero-400/800/1600.svg`, `square/wide/narrow.svg`, `lazy-bottom.svg`) with distinct intrinsic widths so `naturalWidth` assertions are deterministic. |
| `responsive.spec.ts` | Playwright 1.48 spec: candidate selection at 375px and lazy-trigger verification — the same assertions the article shows. |
| `tests/test_fixture.py` | pytest 8.3 suite (stdlib `html.parser`): srcset candidates, sizes/dimensions, eager-vs-lazy attributes, picture fallbacks, alt coverage, preload `imagesrcset`, files on disk. |

## Run the pytest suite

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Expected output:

```text
tests/test_fixture.py::test_srcset_has_three_w_candidates PASSED
tests/test_fixture.py::test_sizes_and_dimensions_present_on_content_images PASSED
tests/test_fixture.py::test_hero_is_eager_and_lazy_is_deferred PASSED
tests/test_fixture.py::test_picture_sources_have_media_and_img_fallback PASSED
tests/test_fixture.py::test_every_content_image_has_alt PASSED
tests/test_fixture.py::test_preload_link_includes_imagesrcset PASSED
tests/test_fixture.py::test_referenced_variants_exist_on_disk PASSED
7 passed
```

## Run the Playwright spec (optional)

```bash
npm i -D @playwright/test
npx playwright install chromium
npx playwright test responsive.spec.ts
```

Serve the directory first (`python -m http.server`) and point `baseURL` or `page.goto` at it — the spec loads `picture.html` relative to this folder.

## Cross-references

- Source article: <https://qapractices.com/test-cases/responsive-image-lazy-loading-testing/> · [Versión ES](https://qapractices.com/es/test-cases/responsive-image-lazy-loading-testing/)
- Metric side: [Core Web Vitals Testing Checklist](https://qapractices.com/checklists/core-web-vitals-testing-checklist/)
