# Testing del Banner de Consentimiento — Companion

Recurso complementario de [Banner de Consentimiento de Cookies: 12 Casos de Prueba](https://qapractices.com/es/test-cases/cookie-consent-banner-testing-test-cases/).

## Contenido

- `consent-gate.mjs` — modelo de consent-gate de CMP sin dependencias: los vendors se registran por categoría (`necessary`/`analytics`/`marketing`), el gate dispara o bloquea cada vendor según el consentimiento almacenado, la versión de política y el scope `addedIn` del vendor (un vendor agregado después del consentimiento no lo hereda). Incluye serialización para persistencia de sesión y default de auto-rechazo con GPC.
- `tests/consent-gate.test.mjs` — subconjunto ejecutable de los casos del artículo: banner en primera visita (TC-01), categorías granulares (TC-02), bloqueo antes del consentimiento (TC-03), disparo tras consentimiento (TC-04), persistencia vía serialize/restore (TC-05), retiro (TC-06), auto-rechazo GPC (TC-10), re-prompt por bump de versión (TC-11), scope de vendor nuevo (TC-12), más edges de consentimiento corrupto y vendor sin categoría.

## Requisitos

- Node.js 20+ (usa el runner `node:test` incorporado — no requiere npm install)

## Uso

```bash
node --test tests/*.test.mjs
```

Salida esperada: `11 passed`.

En un CMP real los mismos checks corren como tests de Playwright contra la capa de red (ver el snippet de Playwright reescrito del artículo) — acá son tests unitarios para que la semántica del consentimiento quede verificable sin navegador.

## Relacionados

- Artículo EN: https://qapractices.com/test-cases/cookie-consent-banner-testing-test-cases/
- Artículo ES: https://qapractices.com/es/test-cases/cookie-consent-banner-testing-test-cases/
