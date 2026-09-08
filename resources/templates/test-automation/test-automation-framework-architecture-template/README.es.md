# Plantilla de Arquitectura de Framework de Automatización — Companion

> Recurso companion de [Plantilla de Arquitectura de Framework de Automatización](https://qapractices.com/es/templates/test-automation-framework-architecture-template) en QAPractices.com.

Framework de automatización en capas con spec files, page objects, utilidades core y workflow de CI para Playwright 1.44 + TypeScript 5.4.

## Requisitos

- Node.js 20+ y npm
- Playwright 1.44+
- TypeScript 5.4+
- GitHub Actions (para CI)

## Setup

```bash
# Instalar dependencias
npm install @playwright/test typescript
npx playwright install chromium

# Correr la suite E2E
npx playwright test

# Correr con un proyecto específico
npx playwright test --project=chromium

# Correr solo smoke tests
npx playwright test --grep @smoke
```

## Archivos

| Archivo | Capa | Propósito |
| ------- | ---- | --------- |
| `tests/e2e/auth/login.spec.ts` | Definición de Tests | Spec file que describe comportamiento de login |
| `pages/LoginPage.ts` | Page Object | Encapsula interacciones de la página de login |
| `core/config/environment.ts` | Core | Configuración aware de ambiente |
| `infra/playwright.config.ts` | Infraestructura | Configuración de Playwright con projects |
| `.github/workflows/e2e-tests.yml` | Infraestructura | Workflow de CI para GitHub Actions |

## Estructura de Proyecto

```text
tests/
└── e2e/
    └── auth/
        └── login.spec.ts

pages/
└── LoginPage.ts

core/
└── config/
    └── environment.ts

infra/
└── playwright.config.ts

.github/
└── workflows/
    └── e2e-tests.yml
```

## Licencia

MIT — libre de usar, modificar y distribuir. Nunca guardes credenciales de producción en config de test; siempre usá variables de entorno.
