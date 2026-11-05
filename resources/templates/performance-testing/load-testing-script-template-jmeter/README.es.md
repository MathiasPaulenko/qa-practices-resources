# Plantilla de Script de Carga con JMeter — Companion

Companion ejecutable de https://qapractices.com/es/templates/load-testing-script-template-jmeter/

## Archivos

- `loadtest.jmx` — test plan de JMeter (thread group, HTTP samplers, aserciones, CSV data set, listeners)
- `users.csv` — datos sintéticos de prueba para `CSVDataSet` (colocar en `testdata/users.csv`)
- `jmeter-load-test.yml` — workflow de GitHub Actions que descarga JMeter 5.6.3 y ejecuta el plan en headless

## Ejecutar

```bash
jmeter -n -t loadtest.jmx -JbaseUrl=https://tu-url-staging -JapiKey=TU_CLAVE -l results.jtl -e -o report/
```

Sobrescribe `baseUrl`/`apiKey` con flags `-J`; nunca hardcodees valores de entorno en el plan.
