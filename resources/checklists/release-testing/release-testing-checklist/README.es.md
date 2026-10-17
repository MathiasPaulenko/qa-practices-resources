# Checklist de Testing de Release — Archivos Complementarios

Companion de [Checklist de Testing de Release](https://qapractices.com/es/checklists/release-testing-checklist/). Un script de smoke post-deploy ejecutable y una plantilla de sign-off de tres compuertas que coincide con las compuertas del checklist.

## Archivos

| Archivo | Propósito |
| ---- | ------- |
| `smoke-test.sh` | Script de smoke post-deployment: parametrizado con `BASE_URL`/`API_KEY`, devuelve código no-cero ante cualquier fallo para bloquear un pipeline o gatillar la evaluación de rollback. |
| `release-signoff-template.md` | Hoja de sign-off imprimible de tres compuertas (pre-release, deployment, post-release) con responsable + hora por ítem, más sección de registro de rollback. |

## Uso

```bash
chmod +x smoke-test.sh
BASE_URL="https://tu-host-de-staging" API_KEY="$STAGING_TOKEN" ./smoke-test.sh
```

Copia `release-signoff-template.md` por release — completa responsables y horarios durante el deploy y archívala con las notas del release.

## Requisitos

- `bash`, `curl` — nada más. El script corre en cualquier pipeline.
