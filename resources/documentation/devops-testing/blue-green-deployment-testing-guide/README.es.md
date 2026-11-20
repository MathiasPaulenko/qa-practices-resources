# Testing de Despliegue Blue-Green — Kit Companion

Scripts ejecutables para cada fase de testing de un despliegue blue-green, companion de la [Guía de Testing de Blue-Green Deployment](https://qapractices.com/es/documentation/blue-green-deployment-testing-guide).

## Contenido

| Archivo | Propósito |
|---|---|
| `green_gate.sh` | Gate de preparación pre-switch: consulta los endpoints de salud de green hasta que todos respondan 200 o se agoten los intentos. |
| `rollout.yaml` | Estrategia `blueGreen` de Argo Rollouts 1.7 con servicio de preview, gate de promoción manual y ventana de 5 minutos con blue caliente. |
| `smoke_test.py` | Smoke test post-switch: verifica los recorridos clave en green y falla rápido ante cualquier no-2xx. |
| `metric_gate.py` | Compara las métricas de green contra la línea base de blue y devuelve promote/rollback. |
| `rollback_drill.py` | Ensayo de rollback: escribe un marcador en green y verifica que sea legible en blue tras el switch (detecta la deriva de esquema). |
| `metrics_baseline.json` / `metrics_green_sample.json` | Snapshots de métricas de ejemplo para el gate. |
| `test_metric_gate.py` | Suite pytest para la lógica del gate de métricas. |

## Requisitos

- Bash + curl para `green_gate.sh` (Linux/macOS/WSL/Git Bash).
- Python 3.10+, solo stdlib. `pytest` para la suite de tests.
- `kubectl` + Argo Rollouts 1.7 para aplicar `rollout.yaml` en un cluster real.

## Uso

```bash
# 1. Pre-switch: bloquea hasta que green esté listo
GREEN_URL=https://green.internal ./green_gate.sh

# 2. Conmuta el tráfico (balanceador, ingress o promote de Argo Rollouts)

# 3. Post-switch: smoke test sobre el color en vivo
TARGET_URL=https://app.internal python smoke_test.py

# 4. Gate de métricas: promueve o revierte
python metric_gate.py metrics_baseline.json metrics_green_sample.json
# exit 0 -> promueve green, exit 1 -> rollback a blue

# 5. Ensayo de rollback (requiere las dos rutas /drill/* descritas en el archivo)
BLUE_URL=http://localhost:8081 GREEN_URL=http://localhost:8082 python rollback_drill.py
```

## Tests

```bash
python -m pytest test_metric_gate.py -v
```

## Umbrales de métricas

`metric_gate.py` compara cada métrica contra un límite expresado como:

- `abs` — delta absoluto (para `error_rate`, donde los deltas relativos sobre tasas mínimas no significan nada). Por defecto: +0.001 (0.1 puntos porcentuales).
- `rel` — delta relativo sobre la línea base. Por defecto: latencia p99 +20%, CPU +15%, memoria +10%.

Ajusta `THRESHOLDS` a tus propias líneas base — los valores por defecto son ejemplos de la guía, no números universales.
