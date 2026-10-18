# Latencia y Throughput de API — Companion Ejecutable

Scripts ejecutables para los [Casos de Test de Latencia y Throughput de API](https://qapractices.com/es/test-cases/api-latency-throughput-test-cases/) de QAPractices.

## Contenido

| Archivo | Propósito |
|---|---|
| `k6-latency.js` | Perfil de carga concurrente (TC-02/TC-03) con umbral `p(95)<500`. |
| `k6-throughput-ramp.js` | Rampa de arrival-rate para encontrar el techo de throughput (TC-02). |
| `jmeter-throughput-assertions.xml` | Fragmento de JMeter con Throughput Controller + Duration Assertion para integrar en un plan de pruebas. |
| `latency-throughput.feature` | Escenarios Gherkin para SLA, saturación y limitación de tasa. |

## Uso

```bash
k6 run k6-latency.js
k6 run k6-throughput-ramp.js

# contra tu propio entorno
API_BASE_URL=https://staging.tu-dominio.com k6 run k6-latency.js
```

Ambos scripts leen `API_BASE_URL` (por defecto `https://api.example.com`, un placeholder — apúntalo a tu entorno de staging). El fragmento de JMeter se integra dentro de un Thread Group junto a tu HTTP Request sampler.

## Fuente

- Recurso: <https://qapractices.com/es/test-cases/api-latency-throughput-test-cases/>
- English version: [README.md](README.md)
