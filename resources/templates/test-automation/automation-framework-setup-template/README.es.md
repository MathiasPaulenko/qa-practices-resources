# Plantilla de Configuración de Framework de Automatización — Companion

> Recurso companion de [Plantilla de Configuración de Framework de Automatización](https://qapractices.com/es/templates/automation-framework-setup-template) en QAPractices.com.

Scaffold copiable para el documento de setup de la primera semana de un framework de automatización: el documento en blanco, un ejemplo rellenado y los archivos de configuración que describe (config de Playwright, plantilla de entorno, reglas de lint, workflow de CI).

## Requisitos

- Node.js 20+ y npm
- Playwright 1.44+
- TypeScript 5.4+
- GitHub Actions (para CI)

## Setup

```bash
# Instalar dependencias
npm install -D @playwright/test typescript dotenv
npx playwright install chromium firefox

# Copiar la plantilla de entorno y rellenar los valores
cp .env.example .env

# Ejecutar la suite
npx playwright test --config infra/playwright.config.ts
```

## Archivos

| Archivo | Propósito |
| ------- | --------- |
| `docs/framework-setup-template.md` | Documento de setup en blanco para copiar a tu repo |
| `docs/framework-setup-shoplite-sample.md` | El mismo documento rellenado para una tienda online ficticia |
| `infra/playwright.config.ts` | Config de Playwright: proyectos chromium + firefox, reintento en CI, `baseURL` desde entorno |
| `.env.example` | Plantilla de variables de entorno comprometida — los secretos reales quedan en CI |
| `eslint.config.mjs` | Config flat que bloquea `waitForTimeout` y selectores CSS en los specs |
| `.github/workflows/e2e-tests.yml` | Workflow de CI: suite de smoke en PRs, regresión completa cada noche |

## Uso

1. Copia `docs/framework-setup-template.md` a tu repo como `docs/framework-setup.md`.
2. Rellena primero la tabla de Decisión de Stack — el resto de secciones dependen de ella.
3. Ajusta los archivos de configuración a tu stack, genera la estructura del repo con `tree -L 3` y pégala en la sección 4.
4. Abre un único PR con el scaffold, los archivos de configuración y el documento rellenado juntos.
