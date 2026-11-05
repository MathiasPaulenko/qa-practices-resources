# Laboratorio de Testing de Feature Flags

Companion ejecutable de la [Guía de Testing de Feature Flags](https://qapractices.com/es/documentation/feature-flags-testing-guide/) — un evaluador de flags solo con stdlib que cubre las cuatro formas de flag de la guía (booleano, por variable de entorno, reglas de targeting + allowlist, rollout porcentual determinista) más suites de Jest 29 para estados del flag, límites de segmentación, determinismo del rollout y manejo de la caída del servicio de flags con MSW 2.x.

## Ejecutar

```bash
npm install
npm test
```

Requiere Node 18+. Las tres suites del evaluador corren en Jest 29; la suite del servicio de flags (`tests/flags-api.test.mjs`) corre en `node:test`, porque MSW 2.x es ESM-only y resuelve limpio con el sistema de módulos propio de Node — sin polyfills de jest.

## Qué cubre

| Suite | Sección de la guía | Qué prueba |
|---|---|---|
| `tests/featureFlags.test.js` | Unit tests + env-var vs SDK | Resolución on/off/undefined/no-booleano, fallback por env-var |
| `tests/segmentation.test.js` | Testing de segmentación | Límites de reglas: plan, país, dispositivo, precedencia del allowlist |
| `tests/rollout.test.js` | Monitoreo del rollout | Buckets sha256 deterministas, split ~50/50, upgrades monótonos, bordes 0%/100% |
| `tests/flags-api.test.mjs` | Servicio de flags mockeado | Flag activo, flag apagado, fallbacks ante HTTP 503 y fallo de red |

## Formas de flag en `featureFlags.js`

- `checkoutV2` — booleano plano, la superficie de unit tests.
- `new-checkout` — respaldado por env-var (`NEW_CHECKOUT`), resuelto al arranque.
- `new-dashboard` — rollout porcentual al 50%, bucketing `sha256(flagKey:userId) mod 100`.
- `ios-widget` — regla de targeting por dispositivo.
- `beta-search` — reglas de plan + país con allowlist explícita.

`launchdarkly-example.js` es un snippet de referencia para la sección de LaunchDarkly — no lo ejecuta la suite.
