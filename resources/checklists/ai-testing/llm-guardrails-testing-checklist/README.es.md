# Checklist de Testing de Guardrails de LLM: Kit Companion

Artefactos ejecutables para el [Checklist de Testing de Guardrails de LLM](https://qapractices.com/es/checklists/llm-guardrails-testing-checklist) de QA Practices.

## Qué contiene

| Archivo | Propósito |
|---------|-----------|
| `guardrails_config.json` | Configuración de políticas: filtro regex de PII, filtro de inyección por keywords, umbral de clasificador de toxicidad |
| `guarded_pipeline.py` | Pipeline simulado que aplica las políticas del config delante de un modelo de prueba — no hace falta un endpoint real |
| `adversarial_prompts.json` | Dataset pequeño escrito a mano: inyección directa, jailbreaks, eco de PII, codificación y un caso seguro de referencia |
| `adversarial_test.py` | Envía el dataset a un endpoint real (`CHAT_API_URL`) y comprueba cada respuesta contra el veredicto esperado |
| `test_guardrails.py` | Suite de pytest que ejecuta el dataset offline contra `guarded_pipeline.py` |
| `requirements.txt` | `requests` + `pytest` |

## Inicio rápido (offline)

```bash
pip install -r requirements.txt
pytest test_guardrails.py -v
```

El pipeline simulado bloquea los prompts que disparan el filtro de inyección por keywords o producen respuestas que coinciden con las regex de PII, así que varios casos del dataset esperan bloqueo.

## Contra un endpoint real

```bash
export CHAT_API_URL=http://localhost:8000/chat
python adversarial_test.py
```

Un prompt cuenta como bloqueado cuando el endpoint responde HTTP 400/401/403/422 o devuelve una frase de rechazo (`I can't`, `I cannot`, ...) en el campo `answer`. El código de salida es distinto de cero si algún caso se desvía de su veredicto esperado.

## Cómo extenderlo

- Añade casos de ataque nuevos a `adversarial_prompts.json` — cada uno necesita `id`, `category`, `prompt`, `expect_blocked`.
- Edita `guardrails_config.json` para que coincida con tu conjunto real de políticas; `guarded_pipeline.py` lo relee al importarse.
- Para más cobertura de ataques, genera casos con el [Prompt de IA: Generar Casos de Test de Guardrails de LLM](https://qapractices.com/es/prompts/ai-prompt-llm-guardrails-test-cases) y valida contra las categorías de AdvBench/HarmBench.
