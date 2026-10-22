# Casos de Prueba de Conversación de Agentes de IA — Companion

Recurso companion de [Casos de Prueba de Agentes de IA: Multi-Turno y Herramientas](https://qapractices.com/es/test-cases/ai-agent-conversation-test-cases/).

## Contenido

- `agent_simulator.py` — modelo determinista solo-stdlib del pipeline de turno del agente descrito en el artículo: guardrails de inyección y contenido dañino, retención de contexto por sesión, un `ToolRegistry` con fallos inyectables, aclaración de parámetros faltantes y detección de bucle por mensajes repetidos. Sin llamadas a APIs de modelos — las reglas suplantan al LLM para que la suite corra completamente offline.
- `tests/conftest.py` — agrega el simulador al `sys.path`.
- `tests/test_agent_simulator.py` — subconjunto ejecutable de los casos del artículo: saludo (TC-001), retención de contexto (TC-002), prompt injection (TC-011), contenido dañino (TC-012), fallo de herramienta (TC-014), conversación circular (TC-018), mensaje vacío (TC-021), aislamiento de sesiones (TC-024), parámetros faltantes (TC-026) y tool call multi-parámetro (TC-004).

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Salida esperada: `10 passed`.

En una suite real apuntarías `send_message` al endpoint HTTP del agente y mantendrías las mismas aserciones — el simulador existe para que las propiedades bajo test (recuerdo, rechazo, elicitación de parámetros, aislamiento) sean visibles sin un modelo en vivo.

## Relacionados

- Artículo EN: https://qapractices.com/test-cases/ai-agent-conversation-test-cases/
- Artículo ES: https://qapractices.com/es/test-cases/ai-agent-conversation-test-cases/
