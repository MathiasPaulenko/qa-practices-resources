# Plantilla de Testing de Distribución Beta de App Móvil — Companion

Artefactos copiables para la [Plantilla de Testing de Distribución Beta de App Móvil](https://qapractices.com/es/templates/mobile-app-beta-distribution-testing-template) de QAPractices.

## Qué contiene

| Ruta | Qué es |
|---|---|
| `docs/beta-distribution-template.md` | El documento de distribución beta en blanco: tracks, matriz de dispositivos, compatibilidad de OS, feedback, métricas de crash, etapas de rollout, gates de release y aprobación. |
| `docs/cartwell-beta-sample.md` | El mismo documento rellenado para CartWell Shopper v4.2.0 — una beta externa de dos semanas en ambas plataformas. |
| `fastlane/Fastfile` | Un lane por track de distribución (`ios_beta_internal`, `ios_beta_external`, `android_beta_internal`, `android_beta_closed`) más `android_rollout` para los porcentajes del rollout escalonado. |
| `.env.example` | Las variables de entorno que leen los lanes: clave API de App Store Connect, ruta de la service account de Play Console, metadatos de la beta y el umbral crash-free. |

## Uso

1. Copia `docs/beta-distribution-template.md` en tu repo por cada ciclo de beta.
2. Copia `fastlane/Fastfile` y `.env.example` en tu proyecto y ajusta scheme, grupos y tracks.
3. Ejecuta un lane por track — `fastlane ios ios_beta_external`, `fastlane android android_beta_closed` — para que la tabla de tracks y la herramienta nunca discrepen en silencio.
4. Para el rollout escalonado: `fastlane android android_rollout percent:0.20` por etapa, gateado por el umbral crash-free de `.env.example`.

## Notas

- Requiere fastlane 2.220+, una clave API de App Store Connect y un JSON de service account de Play Console. Las claves nunca se commitean — las rutas de `.env.example` apuntan a un directorio `keys/` que va al gitignore.
- El release por fases de iOS se activa en App Store Connect, no en fastlane; los porcentajes de rollout de Play Console son el parámetro `rollout:` del track de producción.
