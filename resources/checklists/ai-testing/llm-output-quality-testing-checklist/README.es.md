# Harness de Evaluación de Calidad de Output de LLM

Companion offline del [Checklist de Testing de Calidad de Output de LLM](https://qapractices.com/es/checklists/llm-output-quality-testing-checklist). Puntúa respuestas generadas en las dimensiones del checklist — consistencia, anclaje factual, contradicción y relevancia — sobre un corpus versionado, sin necesitar APIs de pago ni acceso a red.

## Contenido

| Archivo | Propósito |
|---|---|
| `eval_prompts.json` | Corpus de evaluación versionado: 8 prompts mapeados a dimensiones con umbrales |
| `mock_model_outputs.json` | Respuestas grabadas del modelo (3 muestras por prompt) para ejecuciones offline |
| `quality_evaluator.py` | Scorers deterministas: consistencia, grounding, contradicción, relevancia, rechazo |
| `run_evaluation.py` | Ejecutor; puntúa `mock_model_outputs.json` offline o consulta `CHAT_API_URL` en vivo |
| `test_quality_evaluator.py` | Suite pytest para los scorers |

## Inicio rápido

```bash
python -m pytest -v          # tests unitarios de los scorers
python run_evaluation.py     # evaluación offline sobre outputs grabados
```

Modo en vivo contra un endpoint real (requiere `requests`):

```bash
export CHAT_API_URL=http://localhost:8000/chat
python run_evaluation.py
```

Cada prompt se muestrea tres veces para que el scorer de consistencia vea
la varianza real del muestreo. Un caso falla cuando su score baja del
umbral definido en `eval_prompts.json`; añade los fallos de producción al
corpus para que la evaluación se haga más difícil con el tiempo, no más fácil.
