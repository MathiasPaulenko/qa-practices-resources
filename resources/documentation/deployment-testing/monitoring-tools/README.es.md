# Guía de Herramientas de Monitoreo — Scripts Complementarios

Compañero ejecutable de la [Guía de Herramientas de Monitoreo](https://qapractices.com/es/documentation/monitoring-tools/) en QAPractices.

## Contenido

| Archivo | Qué hace |
|---|---|
| `scripts/prometheus-instrumentation.py` | App mínima con `prometheus_client` 0.26.0 que expone `/metrics` con un contador y un histograma, además de tráfico simulado para que los dashboards se muevan. |
| `scripts/alert-rules.yml` | Reglas de alerta de Prometheus que implementan la matriz de severidad P1-P4 de la guía (tasa de error, latencia, disco, flapping de targets). |
| `scripts/otel-node-setup.js` | Arranque de trazas OpenTelemetry para Node.js con el exportador OTLP (`@opentelemetry/sdk-node` 0.301.2) — Jaeger escucha en `:4318` desde la v1.35. |
| `scripts/synthetic-login-check.spec.ts` | Chequeo sintético en Playwright del journey de login, con presupuesto de latencia y credenciales por variables de entorno. Corre en un cron o dentro de Datadog Synthetics / k6. |

## Requisitos

- Python 3.10+ — `pip install prometheus_client==0.26.0`
- Node.js 20+ — `npm i @opentelemetry/sdk-node@0.301.2 @opentelemetry/exporter-trace-otlp-http@0.301.2`
- `@playwright/test` 1.65.1 para el spec sintético

## Uso

```bash
# Endpoint de métricas con tráfico simulado
python scripts/prometheus-instrumentation.py
curl http://localhost:8000/metrics

# Jaeger local para trazas
docker run -p 4318:4318 -p 16686:16686 jaegertracing/all-in-one:1.62
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 node scripts/otel-node-setup.js

# Chequeo sintético contra staging
SYNTH_URL=https://staging.example.internal SYNTH_USER=qa SYNTH_PASS=... \
  npx playwright test scripts/synthetic-login-check.spec.ts
```

Las reglas de alerta se cargan con `rule_files: ["scripts/alert-rules.yml"]` en `prometheus.yml`. Nunca apuntes credenciales sintéticas a una cuenta de usuario real.
