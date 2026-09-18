# Pruebas de Accesibilidad con axe-core — Ejemplos Ejecutables

Repositorio complementario de la guía de QAPractices
[Cómo Realizar Pruebas de Accesibilidad con axe-core](https://qapractices.com/es/documentation/accessibility-testing-axe-core/)
([English version](https://qapractices.com/documentation/accessibility-testing-axe-core/)).

Todos los ejemplos son autocontenidos: la suite de Playwright renderiza fixtures
HTML inline con `page.setContent()` y la de Jest prueba strings de markup — no se
necesita ningún sitio externo ni backend. La suite de Python requiere Chrome local.

## Estructura

```text
playwright/   @axe-core/playwright 4.13.0 + @playwright/test 1.63.0
jest/         jest-axe 11.0.0 + jest 30.5.1
python/       axe-selenium-python 3.0.0 + selenium 4 (requiere Chrome local)
```

## Playwright

```bash
cd playwright
npm install
npx playwright test
```

La config usa `channel: 'chrome'` — ejecuta tu Chrome instalado, sin descargar
navegador. Para CI, quita la opción channel y corre `npx playwright install
chromium` para usar el navegador empaquetado.

Cuatro tests cubren: una página limpia que pasa, un fixture con violaciones
intencionadas (`image-alt`, `color-contrast`, label faltante, `lang` ausente),
gating por impacto (`critical`/`serious`) y un escaneo acotado con `.include()`.
Ojo con el detalle del filtro de tags: `image-alt` es una regla de nivel A — un
set de solo `wcag2aa` la filtra, así que incluye `wcag2a` para cobertura completa.

## Jest (nivel componente)

```bash
cd jest
npm install
npm test
```

jest-axe comprueba markup renderizado sin navegador — primera pasada rápida para
componentes. No puede ver layout, orden de foco ni nada que el navegador calcule:
la regla `color-contrast` no devuelve hallazgos bajo jsdom, así que el contraste
hay que verificarlo con un runner de navegador real como `@axe-core/playwright`.

## Python (Selenium)

```bash
cd python
pip install -r requirements.txt
pytest -v
```

Requiere Chrome/Chromium instalado; Selenium 4 resuelve el driver automáticamente.
Los fixtures se inyectan vía URLs `data:text/html`.

## Versiones verificadas

| Paquete | Versión |
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

Nota: `@axe-core/cypress` y `@axe-core/selenium` **no** existen en npm — la
integración de Cypress es `cypress-axe`, y los usuarios de Selenium necesitan
`@axe-core/webdriverjs` (JS) o `axe-selenium-java` (Java/Maven).
