# Casos de Prueba de Carga y Rendimiento — Companion k6 Ejecutable

Escenarios k6 ejecutables de
[Casos de Prueba de Carga y Rendimiento: 32 Escenarios](https://qapractices.com/es/test-cases/performance-load-testing-test-cases/)
([English version](https://qapractices.com/test-cases/performance-load-testing-test-cases/)).

| Script | Corresponde a | Qué demuestra |
|---|---|---|
| `load-profile.js` | TC-PL-01, 04, 07 | Ramp-up/estable/spike/ramp-down con thresholds de p95/p99 y error |
| `capacity-arrival-rate.js` | TC-PL-18 | Tasa de llegada constante — req/s sostenidos, no solo latencia de VUs |
| `soak-test.js` | TC-PL-12 | Meseta moderada de 4h para exponer leaks y deriva |

## Instalación

Requiere [k6](https://k6.io/) 0.55+. No hay npm install — k6 ejecuta los scripts directamente.

## Ejecución

```bash
k6 run load-profile.js
BASE_URL=https://staging.example-shop.internal k6 run capacity-arrival-rate.js
k6 run soak-test.js
```

Define `BASE_URL` para apuntar a tu servicio; el valor por defecto es `http://localhost:8080`.
Una ejecución sin `thresholds` puede salir con código 0 aunque falle — mantén los
bloques `thresholds` para que CI atrape las regresiones.
