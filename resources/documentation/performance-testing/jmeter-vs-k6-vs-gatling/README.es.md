# JMeter vs k6 vs Gatling — Scripts de Load Test Comparables

Código companion de [JMeter vs k6 vs Gatling: Benchmarks de Rendimiento](https://qapractices.com/es/documentation/jmeter-vs-k6-vs-gatling/) en QAPractices.

## Qué hay dentro

| Carpeta | Herramienta | Versión | Qué muestra |
|---------|-------------|---------|-------------|
| `k6/load-test.js` | k6 | v1.x | Test por etapas (rampa a 20 → sostiene 50 VUs) con thresholds `p(95)<500ms` y tasa de error — sale con código no-cero al romperlos. |
| `gatling/ProductBrowsingSimulation.scala` | Gatling | 3.12 | Escenario equivalente en DSL Scala con assertions de percentil. |
| `jmeter/product-browsing.jmx` | JMeter | 5.6.3 | Plan `.jmx` mínimo: 20 hilos, rampa de 30s, assertion de status, think time de 1s. |

Los tres golpean el mismo endpoint placeholder (`staging.acme-shop.dev/api/v1/products`, sobreescribible con `BASE_URL`) con el mismo perfil — esa es la forma honesta de comparar herramientas: misma carga, motor distinto, mide el generador.

## Ejecutarlos

```bash
# k6 (requiere k6 v1.x)
k6 run --env BASE_URL=https://tu-staging.dev k6/load-test.js

# Gatling (dentro de un proyecto gatling-maven, Gatling 3.12)
mvn gatling:test -Dgatling.simulationClass=ProductBrowsingSimulation -DBASE_URL=https://tu-staging.dev

# JMeter (5.6.3, headless)
jmeter -n -t jmeter/product-browsing.jmx -l results.jtl -e -o report/
```

Nota: los scripts se escribieron contra las APIs documentadas de cada versión pero no se ejecutaron aquí — no hay binarios de load testing en este entorno. El script k6 sigue el contrato `k6/http` + thresholds, el JMX valida contra el schema de JMeter 5.6.3, y el sim de Scala usa el DSL `setup/inject/assertions` de Gatling 3.12.

## Recurso relacionado

- [JMeter vs k6 vs Gatling: Benchmarks de Rendimiento](https://qapractices.com/es/documentation/jmeter-vs-k6-vs-gatling/) — la comparación completa, matriz de decisión e historia de migración que estos scripts soportan.
