# Troubleshooting de Web Testing — Companion

Snippets ejecutables referenciados en la [Guía de Troubleshooting de Web Testing](https://qapractices.com/es/documentation/web-testing-troubleshooting/) de QAPractices.

## Archivos

| Archivo | Problema que resuelve |
|---|---|
| `explicit-waits.js` | Sleeps fijos → waits por condición para pruebas inestables en CI (Problema 1) |
| `stable-selectors.js` | Selectores `data-testid` en lugar de pseudo-clases dependientes del navegador (Problema 2) |
| `playwright-ci.config.ts` | Overrides de timeout, reintentos, viewport y args de lanzamiento para runners de CI más lentos (Problema 3) |
| `visual-mask.js` | Enmascaramiento de elementos para sacar anuncios, timestamps y avatares de los diffs visuales (Problema 4) |
| `shard-ci.sh` | Split de Playwright `--shard` en 4 runners de GitHub Actions (Problema 5) |

## Uso

- Requiere `@playwright/test` 1.65 o superior para los snippets JS/TS.
- `explicit-waits.js` y `stable-selectors.js` exportan helpers pequeños — llámalos desde tus pruebas o adapta el patrón dentro de tus page objects.
- `playwright-ci.config.ts` exporta un objeto `ciProject`; inclúyelo en el array `projects` de tu `playwright.config.ts`.
- `shard-ci.sh` asume una matriz de GitHub Actions con valores `shard` (1..4) y `total` (4).

Sin otras dependencias.
