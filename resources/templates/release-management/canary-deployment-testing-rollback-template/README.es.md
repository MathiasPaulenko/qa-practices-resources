# Decisión de Rollback Canary — Companion Ejecutable

Companion ejecutable de la [Plantilla de Testing y Rollback de Canary Deployment](https://qapractices.com/es/templates/canary-deployment-testing-rollback-template/) en QAPractices.

`rollback_decision.py` es un evaluador stdlib que toma las métricas del canary y devuelve un veredicto `promote` / `hold` / `rollback` con severidad y quien decide — las mismas reglas que los triggers de rollback automático de la plantilla (Sección 6.1) y la matriz de decisión (Sección 7.2).

## Correr los tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

11 tests cubren: promoción en camino feliz, rollback por error rate (umbral y crítico), crash loop de pods, evaluaciones fallidas consecutivas, tiempo máximo de canary, latencia 2x baseline vs sobre umbral (rollback vs hold), hold por tráfico bajo, caída de métrica de negocio y umbrales custom.

## Ejemplo

```python
from rollback_decision import Metrics, evaluate

verdict = evaluate(Metrics(error_rate=2.1, p99_latency_ms=390, request_rate=250))
# Decision.ROLLBACK — "error rate 2.1% above threshold 1.0%" (High, SRE on-call)
```
