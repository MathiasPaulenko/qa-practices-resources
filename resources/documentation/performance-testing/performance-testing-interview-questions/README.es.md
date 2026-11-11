# Companion de Preguntas de Entrevista de Performance Testing

Assets de load testing ejecutables para la guía [30 Preguntas de Entrevista sobre Performance Testing](https://qapractices.com/es/documentation/performance-testing-interview-questions/).

## Requisitos

- [k6 v0.56](https://k6.io/docs/get-started/installation/) o superior
- [Apache JMeter 5.6.x](https://jmeter.apache.org/download_jmeter.cgi) (solo para el runner de CI)
- Una API de staging a la que apuntar `BASE_URL`

## Archivos

| Archivo | Descripción |
| --- | --- |
| `interview-load-test.js` | Script k6 con ramp-up por stages, thresholds de p95/p99 y tasa de error, y login con SharedArray alimentado por CSV |
| `data/users.csv` | Credenciales de ejemplo que consume el script k6 — reemplazar por usuarios reales de staging |
| `jmeter-ci.sh` | Runner non-GUI de JMeter para CI/CD: genera resultados `.jtl` y un reporte HTML |

## Inicio rápido

```bash
# Correr el escenario k6 contra tu API de staging
BASE_URL=https://staging.example.internal k6 run interview-load-test.js

# Correr un plan JMeter headless con reporte HTML
./jmeter-ci.sh my-plan.jmx
```

## Qué demuestra cada archivo

- **Stages y thresholds** — el script sube a 20 usuarios virtuales en 30 segundos, mantiene un minuto y falla cuando `p(95)` supera los 500ms o la tasa de error pasa del 1%, como en Q19 y Q27 de la guía.
- **Parametrización** — `SharedArray` carga `data/users.csv` una sola vez y asigna una fila única a cada usuario virtual con `__VU`, como en Q20.
- **Correlación** — el login corre primero para extraer el token y reutilizarlo, como en Q11 y Q29.
- **Ejecución en CI** — `jmeter-ci.sh` envuelve `jmeter -n -t plan -l results -e -o report`, como en Q15.
