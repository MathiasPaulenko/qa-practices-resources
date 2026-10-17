# Checklist de Gestión de Datos de Testing E2E — Companion Ejecutable

Código companion del [Checklist de Gestión de Datos de Testing E2E](https://qapractices.com/es/checklists/e2e-test-data-management-checklist/) en QAPractices.

## Qué es

Una capa de datos mínima y ejecutable para suites E2E, construida sobre los tres pilares del checklist: creación única, ejecución aislada, limpieza garantizada.

| Archivo | Qué muestra |
|---|---|
| `user.factory.ts` | Factory con emails únicos por invocación (`qa-{ts}-{seq}@test.qapractices.dev`) y helper de limpieza vía API. |
| `seeded-account.fixture.ts` | Fixture de worker Playwright 1.49: hace seed con `request.post`, entrega la cuenta al test y la borra después — incluso en fallo. |
| `seed.sql` | Seed transaccional para datos base; `ON_ERROR_STOP` + `BEGIN/COMMIT` hace que un seed roto nunca deje filas parciales. La limpieza comentada borra por prefijo determinista. |
| `example.spec.ts` | Un test que consume el fixture. |

## Cómo correrlo

```bash
npm install -D @playwright/test@1.49
npx playwright test example.spec.ts   # contra un baseURL que exponga /api/accounts
psql -d e2e_staging -v ON_ERROR_STOP=1 -f seed.sql
```

Apunta `baseURL` en `playwright.config.ts` a un entorno dedicado — nunca a datos de producción.

## Notas de diseño

- Datos únicos por invocación: N workers paralelos nunca tocan la misma fila.
- La limpieza del fixture corre después de `use()` sin importar el resultado del test — sin filas huérfanas.
- El seed SQL envuelve los inserts en una transacción; un statement fallido revierte el lote.
