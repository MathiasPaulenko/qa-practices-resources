# Companion de Performance Testing con JMeter

Recurso companion de la guía [Performance Testing con JMeter](https://qapractices.com/es/documentation/performance-testing-with-jmeter). Incluye un test plan de JMeter listo para ejecutar, datos CSV de test, un script de aserción de SLA y un workflow de GitHub Actions.

## Archivos

| Archivo | Propósito |
| ------ | --------- |
| `test-plans/checkout-load.jmx` | Test plan de JMeter para load testing de checkout (100 threads, 60s ramp-up) |
| `test-data/checkout-users.csv` | CSV data set con usuarios de checkout realistas |
| `scripts/assert-sla.py` | Script Python para asertar p95 y error rate desde resultados JTL |
| `.github/workflows/perf-tests.yml` | Workflow de GitHub Actions que ejecuta JMeter nocturno |

## Inicio Rápido

```bash
# Descargar JMeter 5.6.3
wget https://dlcdn.apache.org/jmeter/binaries/apache-jmeter-5.6.3.tgz
tar -xzf apache-jmeter-5.6.3.tgz

# Ejecutar el test de carga en modo CLI
./apache-jmeter-5.6.3/bin/jmeter \
  -n -t test-plans/checkout-load.jmx \
  -l results/checkout.jtl \
  -e -o report/ \
  -JdataDir=./test-data

# Asertar SLA desde los resultados
python scripts/assert-sla.py \
  --jtl results/checkout.jtl \
  --max-p95 1000 \
  --max-error-rate 0.5
```

## Requisitos

- Apache JMeter 5.6.3
- Python 3.11+
- Un servidor API destino (default: `api.staging.local:8080`)
