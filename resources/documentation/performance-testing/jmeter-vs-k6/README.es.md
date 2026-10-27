# JMeter vs k6 — Scripts Ejecutables del Flujo de Pagos

Código companion de la guía [JMeter vs k6: Cómo Elegir Herramienta de Carga](https://qapractices.com/es/documentation/jmeter-vs-k6/) — los artefactos ejecutables detrás de la decisión de NovaPay: 50.000 usuarios virtuales, un ramp escalonado y un setup híbrido JMeter + k6.

## Contenido

| Ruta | Qué es |
|---|---|
| `k6/payments.js` | Script de k6 v1.x: `ramping-vus` hasta 50k VUs, thresholds de p95 y tasa de error, flujo pago → reembolso, think time de ~40 s. |
| `jmeter/jsr223-payment-sampler.groovy` | JSR223 Sampler + PostProcessor de JMeter 5.6.3: construye el JSON de pago y extrae el `transactionId`. |
| `ci/jmeter-v1-load-test.yml` | Workflow de GitHub Actions que corre la suite `.jmx` en modo non-GUI y aserta sobre la tasa de error del JTL. |
| `ci/k6-v2-load-test.yml` | Workflow de GitHub Actions con `grafana/k6-action@v0.3.1` y salida a InfluxDB. |
| `scripts/assert-jtl.sh` | Gate en Bash que falla el build cuando la tasa de error del JTL supera la fracción indicada. |

## Uso

```bash
# k6 — requiere k6 v1.x y un BASE_URL alcanzable
NOVA_API_KEY=tu-clave BASE_URL=https://staging.api.local/v2 \
  k6 run k6/payments.js

# JMeter — modo non-GUI, JTL + reporte HTML
jmeter -n -t jmeter/v1-payments.jmx -l results.jtl -e -o report/

# Aserción sobre la tasa de error del JTL (< 0,5%)
./scripts/assert-jtl.sh results.jtl 0.005
```

Copiá los archivos de `ci/` a `.github/workflows/` de tu repo para activarlos — viven fuera de `.github/` a propósito para que nunca se disparen en este repositorio.

`api.novapay.example.com` e `influxdb.novapay-sandbox` son placeholders; reemplazalos por tu URL de staging y tu endpoint interno de InfluxDB.
