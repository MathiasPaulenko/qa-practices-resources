# Load vs Stress vs Spike Testing — Perfiles Ejecutables

Código complementario de [Stress vs Load vs Spike Testing: Diferencias Clave](https://qapractices.com/es/documentation/stress-testing-vs-load-testing-vs-spike-testing/) en QAPractices.

## Qué incluye

| Archivo | Herramienta | Versión | Forma de carga |
|---------|-------------|---------|----------------|
| `k6/load-test.js` | k6 | 1.x | Ramp a 50 VUs, meseta de 5 minutos, ramp down — con thresholds `p(95)<500ms` y de tasa de errores. |
| `k6/stress-test.js` | k6 | 1.x | `ramping-vus` subiendo de 50 a 800 VUs sin thresholds de aborto — el punto del stress test es llegar al fallo y luego observar la recuperación. |
| `k6/spike-test.js` | k6 | 1.x | `ramping-arrival-rate`: base de 100 rps, salto de 10 segundos a 1.000 rps, retención de 2 minutos, caída para observar la recuperación. |
| `jmeter/test-plan.jmx` | JMeter | 5.6.3 | Plan headless mínimo: 50 threads, ramp de 120 s, duración de 420 s, aserción de status, think time de 1 s. |

Todos los scripts apuntan al mismo endpoint placeholder (`https://api.staging.acme-shop.dev/api/v1/products`, sobreescribible con `BASE_URL`). Mismo objetivo, distinta forma de carga — eso es lo que separa los tres tipos de test, no la herramienta.

## Cómo ejecutarlos

```bash
# k6 (requiere k6 v1.x)
k6 run --env BASE_URL=https://your-staging.dev k6/load-test.js
k6 run --env BASE_URL=https://your-staging.dev k6/stress-test.js
k6 run --env BASE_URL=https://your-staging.dev k6/spike-test.js

# JMeter 5.6.3 (headless, reporte HTML)
jmeter -n -t jmeter/test-plan.jmx -l results.jtl -e -o report/
```

Notas:

- El script de stress no declara thresholds a propósito — abortar por errores frenaría el test antes del punto de ruptura que existe para encontrar.
- Para carga escalonada o instantánea en JMeter, instalá el plugin Ultimate Thread Group (`jpgc-plugins`); el plan incluido cubre el perfil de carga.
- Los scripts se escribieron contra las APIs documentadas de k6 1.x y JMeter 5.6.3, pero no se ejecutaron aquí — no hay binarios de load testing en este entorno.

## Recurso relacionado

- [Stress vs Load vs Spike Testing: Diferencias Clave](https://qapractices.com/es/documentation/stress-testing-vs-load-testing-vs-spike-testing/) — objetivos, metodología, métricas clave y la matriz comparativa que estos scripts acompañan.
