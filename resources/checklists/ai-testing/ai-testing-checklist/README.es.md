# Checklist de Testing de IA — Companion Ejecutable

Repositorio complementario del recurso de QAPractices
[Checklist de Testing de IA: LLM, Alucinaciones y Seguridad](https://qapractices.com/es/checklists/ai-testing-checklist/)
([English version](https://qapractices.com/checklists/ai-testing-checklist/)).

Dos modos: `eval_runner.py` corre el dataset de guardrails contra la API
real de OpenAI, y `mock_llm.MockClient` da respuestas deterministas para
que la suite de pytest funcione offline sin API key.

## Estructura

```text
eval_runner.py          verificador de frases esperadas/prohibidas (openai 1.x o mock)
mock_llm.py             cliente mock determinista que imita la API de OpenAI
guardrail_dataset.json  dataset inicial: input, frases esperadas, frases prohibidas
tests/test_eval_runner.py suite pytest 8.3 para el comportamiento del runner
requirements.txt        openai>=1.54, pytest>=8.3
```

## Ejecutar

```bash
pip install -r requirements.txt

# tests offline (sin API key)
pytest tests/ -v

# corrida offline del dataset contra el mock
python eval_runner.py --mock

# corrida real contra la API
export OPENAI_API_KEY=sk-...
python eval_runner.py --model gpt-4o-mini
```

## Qué cubren los tests

- **Frases esperadas pasan** — una respuesta con los términos requeridos evalúa limpio.
- **Contenido esperado ausente falla** — AssertionError cuando falta un término requerido.
- **Contenido prohibido falla** — AssertionError cuando aparece una frase prohibida.
- **Matching insensible a mayúsculas** — respuestas en mayúsculas matchean patrones en minúscula.
- **Reporte por dataset** — cada caso reporta pass/fail sin frenar la corrida.
- **Fallo aislado** — un caso que falla se reporta, no se levanta, en `run_dataset`.

Los seis tests pasan offline con pytest 8.3 — el mock mantiene al runner
determinista conservando la interfaz del cliente de OpenAI.
