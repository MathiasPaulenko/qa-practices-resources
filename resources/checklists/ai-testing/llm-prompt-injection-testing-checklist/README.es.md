# Checklist de Pruebas de Prompt Injection en LLM — Kit Complementario

Complemento ejecutable de la [Checklist de Pruebas de Prompt Injection en LLM](https://qapractices.com/es/checklists/llm-prompt-injection-testing-checklist). Empaqueta el harness de sondas, el dataset adversarial y la verificación de guardrail del recurso en una suite pytest que corre offline contra un LLM simulado — o contra un endpoint real si defines `LLM_ENDPOINT`.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `probe.py` | Harness de sonda estilo chat-completions (`requests` 2.32+). Lee `LLM_ENDPOINT` del entorno. |
| `mock_llm.py` | Mock determinista de un modelo endurecido: rechaza marcadores de inyección, responde entradas benignas. |
| `guardrail.py` | `assert_no_disclosure` — falla si aparecen términos prohibidos en la salida del modelo. |
| `dataset.yaml` | Prompts adversariales con `name`, `input` y `expectation` (`refuse` / `allow`). |
| `test_probe.py` | Ejecución pytest parametrizada sobre el dataset; mock por defecto, endpoint real por variable de entorno. |
| `requirements.txt` | Dependencias fijadas (`requests`, `pytest`, `PyYAML`). |

## Uso

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecución offline contra el mock incluido
pytest test_probe.py -v

# Ejecución contra un endpoint real de chat-completions
LLM_ENDPOINT=https://tu-gateway-llm.interno/v1/chat pytest test_probe.py -v
```

## Requisitos

- Python 3.10+
- `requests` 2.32+
- `pytest` 9.x
- `PyYAML` 6.x

## Notas

- El mock simula un modelo *endurecido*: rechaza los marcadores de inyección de `mock_llm.INJECTION_MARKERS`. Un test que falla contra el mock indica un problema en el harness o el dataset, no en el modelo.
- Para evaluar un modelo vulnerable, apunta `LLM_ENDPOINT` a un gateway de staging y lee los fallos como hallazgos — clasifícalos con la escala de severidad de la checklist.
- Amplía `dataset.yaml` en cada release; una entrada por vector de ataque y etiqueta el archivo por versión de modelo.
