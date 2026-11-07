# Herramientas de Pruebas de Accesibilidad — Ejemplos ejecutables

Código complementario de [Herramientas de Pruebas de Accesibilidad: WAVE, Lighthouse y axe-core](https://qapractices.com/es/documentation/accessibility-testing-tools/) en QAPractices.

Tres piezas ejecutables que cubren el lado automatizado de la guía — el lado manual (NVDA, pasadas de teclado, muestreo de contraste) está explicado paso a paso en el artículo.

## Qué incluye

| Ruta | Qué hace |
|---|---|
| `playwright/` | Spec con `@axe-core/playwright` 4.10: escaneo de página completa, escaneo acotado (include/exclude/widgets), filtrado por tags WCAG, chequeo de contraste con una sola regla |
| `ci/fail-build-if-a11y-fails.js` | Gate de CI que filtra violaciones de axe por `impact` (critical/serious bloquean, moderate/minor advierten) |
| `ci/lighthouserc.json` | Config de Lighthouse CI 0.14: aserciones solo de accesibilidad con score >= 90 |
| `python/wave_api_check.py` | Llamada a la API de WAVE que imprime conteos de error/contrast/alert para una URL |

## Inicio rápido

```bash
# Playwright + axe-core
cd playwright && npm install && npx playwright install chromium
npx playwright test

# Gate de CI (ejecutar dentro de tu harness de axe)
node ci/fail-build-if-a11y-fails.js < axe-results.json

# Auditoría solo de accesibilidad con Lighthouse
npm install -g @lhci/cli@0.14.x
lhci autorun --config=ci/lighthouserc.json

# API de WAVE (necesita una key de wave.webaim.org)
pip install -r python/requirements.txt
WAVE_API_KEY=tu-key python python/wave_api_check.py https://staging.tutienda.com
```

## Notas

- La spec de Playwright espera un dev server local o una URL de staging — apuntá `BASE_URL` a la tuya.
- `your-wave-api-key` es un placeholder: conseguí una real en [wave.webaim.org/api](https://wave.webaim.org/api/).
- Para la toolchain completa de axe-core (Jest, Selenium/Python, fixtures con violaciones intencionadas), mirá el companion hermano [accessibility-testing-axe-core](../accessibility-testing-axe-core/).
