# Pruebas de Carga — Ejemplos ejecutables

Versiones ejecutables de los tres ejemplos del artículo
[Guía de Pruebas de Carga: Técnicas Prácticas](https://qapractices.com/es/documentation/load-testing/).

## Contenido

| Archivo | Qué hace |
|---|---|
| `load-test.js` | Perfil de rampa completo en k6: 5 stages (rampa, estable, rampa, estable, bajada) con umbrales de `http_req_duration` y `http_req_failed` que rompen la ejecución. URL objetivo vía variable `BASE_URL`. |
| `run-jmeter.sh` | Runner de Apache JMeter 5.6.x en modo non-GUI: ejecuta un plan `.jmx`, escribe `results.jtl` y un reporte HTML. |
| `github-actions/k6-smoke.yml` | Job de GitHub Actions que corre una carga smoke de 60 segundos y 20 VUs dentro de la imagen oficial `grafana/k6` en cada PR. |

## Uso

```bash
k6 run -e BASE_URL=https://staging.example.com load-test.js
./run-jmeter.sh load-test-plan.jmx report/
```

Para el job de GitHub Actions, copiá `github-actions/k6-smoke.yml` dentro de
`.github/workflows/` en tu repositorio y apuntá la URL a tu entorno de
staging. Mantené la corrida smoke bajo dos minutos — su trabajo es detectar
regresiones catastróficas, no medir capacidad.

## Requisitos

- k6 2.x — `brew install k6` / `winget install k6` o la imagen Docker `grafana/k6`
- Apache JMeter 5.6.x para `run-jmeter.sh`
- Docker (para el job smoke de CI y para correr k6 containerizado)
