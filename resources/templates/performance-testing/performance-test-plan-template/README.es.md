# Plantilla de Plan de Pruebas de Rendimiento — Scripts Companion

Scripts companion para la [Plantilla de Plan de Pruebas de Rendimiento](https://qapractices.com/es/templates/performance-test-plan-template).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `scripts/checkout-load-test.js` | k6 0.54 prueba de carga normal: 200 VUs por 30 minutos. |
| `scripts/checkout-stress-test.js` | k6 0.54 prueba de stress: carga incremental de 500 a 2000 VUs. |
| `scripts/checkout-soak-test.js` | k6 0.54 prueba de soak: 200 VUs por 12 horas. |
| `scripts/checkout-spike-test.js` | k6 0.54 prueba de spike: 100 a 1000 VUs en 1 minuto. |
| `scripts/jmeter-checkout-load-test.jmx` | JMeter 5.6 plan de prueba non-GUI para API de checkout. |

## Uso

```bash
# Instalar k6 0.54
# macOS: brew install k6
# Linux: ver README.md

# Correr prueba de carga normal
k6 run --vus 200 --duration 30m --out json=results.json scripts/checkout-load-test.js

# Correr prueba de stress
k6 run scripts/checkout-stress-test.js

# Correr prueba de soak
k6 run scripts/checkout-soak-test.js

# Correr prueba de spike
k6 run scripts/checkout-spike-test.js

# Correr prueba de JMeter (non-GUI)
jmeter -n -t scripts/jmeter-checkout-load-test.jmx -l results.jtl -e -o dashboard/
```

## Requisitos

- k6 0.54+
- JMeter 5.6+
- Node.js 20+ (para módulos ES de k6)
