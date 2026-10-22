# Casos de Prueba de Imágenes Responsive y Lazy Load — Companion Ejecutable

Las piezas ejecutables detrás de la página [Casos de Prueba de Imágenes Responsive](https://qapractices.com/es/test-cases/responsive-image-lazy-loading-testing/) de QAPractices: un fixture `picture.html` que ejercita srcset/`sizes`, art direction con `<picture>`, carga eager/lazy y un caso de imagen rota — más una spec Playwright y una suite pytest que verifica los contratos de markup del fixture.

## Contenido

| Archivo | Qué es |
|---|---|
| `picture.html` | Fixture sin dependencias: hero srcset (eager, `fetchpriority="high"`, precargado), bloque `<picture>` de art direction, imagen rota intencional y una imagen lazy ~2000px debajo del pliegue. |
| `img/` | Variantes SVG (`hero-400/800/1600.svg`, `square/wide/narrow.svg`, `lazy-bottom.svg`) con anchos intrínsecos distintos para que las aserciones de `naturalWidth` sean determinísticas. |
| `responsive.spec.ts` | Spec Playwright 1.48: selección de candidato a 375px y verificación del trigger lazy — las mismas aserciones que muestra el artículo. |
| `tests/test_fixture.py` | Suite pytest 8.3 (stdlib `html.parser`): candidatos srcset, sizes/dimensiones, atributos eager-vs-lazy, fallbacks de picture, cobertura de alt, `imagesrcset` del preload, archivos en disco. |

## Correr la suite pytest

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Salida esperada:

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

## Correr la spec Playwright (opcional)

```bash
npm i -D @playwright/test
npx playwright install chromium
npx playwright test responsive.spec.ts
```

Serví el directorio primero (`python -m http.server`) y apuntá `baseURL` o `page.goto` ahí — la spec carga `picture.html` relativo a esta carpeta.

## Referencias cruzadas

- Artículo fuente: <https://qapractices.com/es/test-cases/responsive-image-lazy-loading-testing/> · [EN version](https://qapractices.com/test-cases/responsive-image-lazy-loading-testing/)
- Lado de métricas: [Checklist de Core Web Vitals](https://qapractices.com/es/checklists/core-web-vitals-testing-checklist/)
