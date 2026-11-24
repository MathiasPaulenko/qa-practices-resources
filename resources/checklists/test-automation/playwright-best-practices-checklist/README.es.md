# Checklist de Buenas Prácticas de Playwright — Companion

Scaffolding ejecutable para la [Checklist de Buenas Prácticas de Playwright](https://qapractices.com/es/checklists/playwright-best-practices-checklist).

## Archivos

- `playwright.config.ts` — config consciente de CI: `retries`/`forbidOnly`/`workers` según `process.env.CI`, `trace: 'on-first-retry'`, screenshot+vídeo en fallo, `baseURL` por entorno, `testIdAttribute` y matriz Chromium/WebKit/móvil detrás de un proyecto `setup` que genera `storageState`.
- `fixtures.ts` — preparación compartida vía `test.extend`: fixture `authedPage` que evita el login por UI, y fixture `data` que crea un proyecto aislado por test por API y lo limpia en el teardown.
- `github_actions_playwright.yml` — shard de 4 vías con reporters `blob` fusionados en un reporte HTML vía `merge-reports`.

## Uso

```bash
cp playwright.config.ts <repo>/playwright.config.ts
cp fixtures.ts <repo>/tests/fixtures.ts
cp github_actions_playwright.yml <repo>/.github/workflows/playwright.yml
npm ci && npx playwright install --with-deps
npx playwright test
```

Requisitos: `BASE_URL` y `API_URL` definidas por entorno; un proyecto `*.setup.ts` hace el login una vez y escribe `playwright/.auth/user.json`.
