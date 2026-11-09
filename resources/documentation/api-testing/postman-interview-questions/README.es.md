# Top 20 Preguntas de Entrevista Postman — Recursos Companion

Recursos complementarios de la guía [Top 20 Preguntas de Entrevista Postman: API FinFlow](https://qapractices.com/es/documentation/postman-interview-questions/) en QAPractices.com.

Los archivos reproducen el escenario FinFlow usado en toda la guía: una colección `FinFlow-Payments-v3` con carpetas `Auth`, `Payments`, `Refunds` y `Webhooks`, un pre-request script a nivel de colección que calcula el header HMAC `X-Request-Signature`, un environment de staging y los archivos de datos que mencionan las preguntas de Newman y testing data-driven.

## Contenido

| Archivo | Descripción |
| --- | --- |
| `collections/FinFlow-Payments-v3.json` | Colección Postman v2.1: 4 carpetas, peticiones encadenadas (`login → createPayment → getPayment → createRefund`), aserciones `pm.test` sobre status, `processorCode`, `idempotency_key`, `retryCount` y el SLA de 600 ms. |
| `environments/staging.json` | Environment de staging con `base_url`, `api_key`, `auth_token`, `token_expiry` y `correlation_id`. Los dominios `*.finflow.example` son ficticios: apuntalos a tu propio mock o API de staging. |
| `data/payments-test-data.csv` | 120 filas de datos de pago para ejecuciones `newman -d`: pagos válidos, monedas inválidas, tokens expirados y casos de `idempotency_key` duplicado. |
| `data/refunds-edge-cases.json` | Edge cases de reintento de reembolso del caso de estudio (`correlation_id` expirado, montos negativos, reintentos). |
| `.github/workflows/api-tests.yml` | Workflow de GitHub Actions que instala Newman 6 y bloquea pull requests contra `staging`. |

## Requisitos

- Postman v11 (GUI) o Newman 6.x (CLI)
- Node.js 20 LTS

## Inicio Rápido

Importá la colección y el environment en Postman:

1. Abrí Postman v11
2. Hacé click en **Import** y seleccioná `collections/FinFlow-Payments-v3.json`
3. Hacé click en **Import** otra vez y seleccioná `environments/staging.json`
4. Elegí el environment **FinFlow Staging** en el desplegable
5. Seteá `merchant_secret` como variable de colección (la colección trae un valor placeholder)
6. Ejecutá primero **Auth > POST /auth/login** para que el test script guarde `auth_token`

## Ejecutar con Newman (CLI)

```bash
# Instalar Newman 6.x
npm install -g newman@6
npm install -g newman-reporter-htmlextra

# Ejecución data-driven completa (120 iteraciones)
newman run collections/FinFlow-Payments-v3.json \
  -e environments/staging.json \
  -d data/payments-test-data.csv \
  --reporters cli,junit,htmlextra

# Solo la carpeta Refunds con edge cases — el comando del caso de estudio
newman run collections/FinFlow-Payments-v3.json \
  -e environments/staging.json \
  -d data/refunds-edge-cases.json \
  --folder Refunds
```

> **Nota:** las URLs `*.finflow.example` son placeholders. Para ver respuestas reales, corré la colección contra un mock local (por ejemplo `json-server` o un mock server de Postman) y actualizá `base_url` en `environments/staging.json`.

## Integración CI/CD (GitHub Actions)

`.github/workflows/api-tests.yml` corre en cada PR contra `staging` y todas las noches a las 03:00 UTC: instala Newman 6, ejecuta la suite data-driven completa, exporta reportes JUnit + htmlextra y los sube como artifacts. Copialo en la carpeta `.github/workflows/` de tu repo.

## Recursos Relacionados

- [Top 20 Preguntas de Entrevista Postman: API FinFlow](https://qapractices.com/es/documentation/postman-interview-questions/)
- [Cómo Testear APIs REST con Postman](https://qapractices.com/es/documentation/how-to-test-rest-api-postman/)
- [Guía de API Testing](https://qapractices.com/es/documentation/api-testing-guide/)
