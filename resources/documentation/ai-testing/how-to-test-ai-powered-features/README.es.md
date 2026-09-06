# Cómo Probar Funcionalidades con IA — Companion

Archivos companion para la [guía de How to Test AI-Powered Features](https://qapractices.com/es/documentation/how-to-test-ai-powered-features).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `tests/golden-dataset.json` | Dataset dorado curado con 2 ejemplos de sentiment (expandir a 50-200 para producción). |
| `tests/test_model_contract.py` | Contract test: esquema, código de estado, latencia, rango de confianza. |
| `tests/test_sentiment_behavior.py` | Aserciones basadas en propiedades: etiqueta en rango esperado, confianza above mínimo. |
| `tests/test_model_drift.py` | Detección de drift: calcula F1 sobre el dataset dorado y bloquea deploy por debajo de la línea base. |
| `tests/test_shadow_comparison.py` | Shadow test: compara modelo actual vs. candidato sobre la misma entrada. |
| `tests/test_adversarial_robustness.py` | Robustez adversaria: vacío, sin sentido, largo, ambiguo, no inglés, contradictorio. |

## Requisitos

- Python 3.10+
- pytest 8.3+
- requests 2.32+

## Uso

1. Copiá el directorio `tests/` a tu proyecto.
2. Actualizá `BASE_URL` en cada archivo de test para apuntar a tu API de staging.
3. Expandí `golden-dataset.json` con 50-200 entradas representativas.
4. Ejecutá `pytest tests/ -v` para correr todos los tests.
5. En la primera ejecución, generá las líneas base para F1 y umbrales de confianza.
6. Bloqueá deploys cuando los tests de drift fallen.

## Integración de CI

```yaml
- run: pytest tests/ -v --tb=short
```
