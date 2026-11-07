# Guía de Testing de Accesibilidad WCAG — Ejemplos ejecutables

Código companion de la [Guía de Testing de Accesibilidad WCAG](https://qapractices.com/es/documentation/accessibility-wcag-testing-guide/). Cada ejemplo mapea una técnica de verificación WCAG 2.2 de la guía a un chequeo ejecutable.

## Estructura

| Ruta | Qué cubre |
|---|---|
| `playwright/tests/pour-rules.spec.js` | Reglas de axe-core agrupadas por principio POUR — escaneos dirigidos en vez de una pasada gigante |
| `playwright/tests/dom-checks.spec.js` | Dos chequeos DOM baratos que los escáneres no ven: jerarquía de headings y asociación de labels |
| `jest-axe/login-form.test.jsx` | Aserción jest-axe a nivel de componente dentro de una suite Jest + Testing Library |
| `ci/lighthouserc.js` | Aserciones de Lighthouse CI como gate de la categoría de accesibilidad |
| `ci/accessibility-tests.yml` | Job de GitHub Actions: axe CLI en páginas críticas + Lighthouse autorun |

## Correr los specs de Playwright

```bash
cd playwright
npm install
npx playwright test
```

Ambos specs pegan contra `BASE_URL` (por defecto `http://localhost:3000`). Apuntalos a un staging:

```bash
BASE_URL=https://staging.example.com npx playwright test
```

## Correr el test de jest-axe

```bash
cd jest-axe
npm install --save-dev jest @testing-library/react jest-axe@9
npx jest login-form.test.jsx
```

El spec espera un componente `LoginForm` en scope — cambiá el import por un componente real de tu app.

## Gate de CI

Copiá `ci/accessibility-tests.yml` a `.github/workflows/` y `ci/lighthouserc.js` a la raíz del repo. El job escanea tres páginas críticas con `@axe-core/cli` y falla ante cualquier violación, después corre `lhci autorun` para el score de la categoría de accesibilidad (≥0.95).

Acotá el gate a WCAG 2.2 A/AA en flujos críticos primero — un gate que falla por AAA o hallazgos menores se desactiva dentro de un sprint.
