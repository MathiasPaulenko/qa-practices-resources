# Guía de Testing de Sistemas Multi-Agente AI — Companion Ejecutable

Repositorio companion del recurso de QAPractices
[Guía de Testing de Sistemas Multi-Agente AI](https://qapractices.com/es/documentation/multi-agent-ai-systems-testing-guide/)
([English version](https://qapractices.com/documentation/multi-agent-ai-systems-testing-guide/)).

`agent_kit.py` incluye fixtures mínimos en Python puro — un bus de
mensajes, una función de voto mayoritario, una herramienta compartida con
estado por agente, un detector de deadlocks por grafo de espera, un
enjambre de juguete y un orquestador con reintentos — así que la suite
pytest no necesita LLM, API key ni instalación de ningún framework.

## Estructura

```text
agent_kit.py              bus de mensajes, votación, herramienta compartida, detector de deadlocks, enjambre, orquestador
tests/test_multi_agent.py suite pytest 8.3 que implementa las matrices de test de la guía
requirements.txt          pytest>=8.3 (única dependencia)
```

## Ejecutar

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Qué cubren los tests

- **Validación de mensajes** — los payloads malformados se rechazan y los
  mensajes desordenados se reordenan por número de secuencia.
- **Orquestación** — un workflow investigar-luego-escribir ejecuta ambos
  agentes, y un agente inestable se reintenta hasta que la corrida pasa.
- **Consenso** — un agente bizantino no puede invertir una mayoría honesta,
  y el quorum bloquea la decisión cuando votan muy pocos agentes.
- **Conflictos** — el estado de la herramienta compartida queda aislado por
  agente, y una espera circular entre dos agentes se marca como deadlock.
- **Comportamiento emergente** — la métrica global del enjambre converge en
  100 iteraciones y el trabajo continúa tras perder un agente.

Los 12 tests pasan offline con pytest 8.3 — todos los fixtures son
determinísticos, así que la suite es segura para CI.
