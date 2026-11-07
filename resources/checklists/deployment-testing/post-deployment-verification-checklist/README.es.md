# Checklist de Verificación Post-Deploy — Companion

Companion ejecutable del recurso [Checklist de Verificación Post-Deploy](https://qapractices.com/es/checklists/post-deployment-verification-checklist).

Los tres scripts cubren la parte ejecutable de la checklist: el health probe, la pasada de smoke con k6 y un spec mínimo de Playwright para el flujo crítico — todo manejado por la variable de entorno `BASE_URL` para que nada apunte a un host hardcodeado.

## Archivos

| Archivo | Contenido |
|---|---|
| `health-check.sh` | Check con curl + jq de que `/health` retorna 200 y los componentes requeridos reportan `up` |
| `smoke-test.js` | Smoke test con k6 (5 VUs, 30s) con umbrales de latencia p95 y error rate |
| `post-deployment-verification.spec.ts` | Spec de Playwright que cubre el endpoint de health y el render de una página crítica |

## Uso

- `BASE_URL=https://api.yourdomain.com ./health-check.sh` — corré apenas termina el deploy; falla ante un no-200 o cualquier componente que no esté `up`.
- `k6 run -e BASE_URL=https://api.yourdomain.com smoke-test.js` — pasada corta de carga; el build falla si p95 > 500ms o errores > 1%.
- `BASE_URL=https://app.yourdomain.com npx playwright test post-deployment-verification.spec.ts --reporter=list` — check del flujo crítico.
- Conectá `health-check.sh` y `smoke-test.js` al pipeline como gates post-deploy; el spec de Playwright dejalo para releases que tocan UI.
- Los umbrales son puntos de partida — definí los números de rollback de tu equipo antes de deployar, como pide la sección 9 de la checklist.

Recurso en el sitio: [qapractices.com/es/checklists/post-deployment-verification-checklist](https://qapractices.com/es/checklists/post-deployment-verification-checklist)
