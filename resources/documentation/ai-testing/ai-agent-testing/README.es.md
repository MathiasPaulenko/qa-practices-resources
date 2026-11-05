# AI Agent Testing — Archivos Complementarios

Ejemplos ejecutables de [Guía de Testing de Agentes IA: Autónomos y Multi-Agente](https://qapractices.com/es/documentation/ai-agent-testing/).

## Contenido

- `tests/test_llm_output_eval.py` — valida la respuesta de un chatbot de soporte contra un esquema JSON y exige citas (Python 3.11, pytest 8.2, jsonschema 4.22).
- `tests/test_agent_trace.py` — replay de un trace de agente grabado y aserciones sobre la secuencia de tool calls y el estado final.
- `tests/requirements.txt` — dependencias fijadas.

## Setup

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r tests/requirements.txt
```

`qa_assistant` y `agent` son placeholders de tus propios wrappers cliente alrededor del endpoint del modelo y del harness del agente — reemplazá los imports con tu implementación antes de ejecutar.
