# Testing de Temperature y Top-P en LLMs — Companion Ejecutable

Repositorio complementario del recurso de QAPractices
[Testing de temperature y top-p en LLMs](https://qapractices.com/es/documentation/llm-temperature-top-p-testing-guide/)
([English version](https://qapractices.com/documentation/llm-temperature-top-p-testing-guide/)).

Dos modos: `sweep.py` corre la grilla temperature x top-p contra la API real
de OpenAI, y `mock_llm.MockClient` simula el mismo comportamiento de sampling
offline para que la suite de pytest no necesite API key.

## Estructura

```text
sweep.py            runner de la grilla temperature x top-p (cliente openai 1.x o mock)
mock_llm.py         cliente mock determinista que simula el sampling
tests/test_sweep.py suite pytest 8.3 del comportamiento del barrido
requirements.txt    openai>=1.54, pytest>=8.3
```

## Ejecutar

```bash
pip install -r requirements.txt

# tests offline (sin API key)
pytest tests/ -v

# barrido offline
python sweep.py --mock

# barrido contra la API real
export OPENAI_API_KEY=sk-...
python sweep.py
```

## Qué cubren los tests

- **Determinismo en temp 0** — diez corridas, un solo output único.
- **Diversidad en temp 1.0** — diez corridas, más de un output único.
- **Truncamiento de top-p** — `top_p=0.2` limita las variantes alcanzables a dos.
- **Cobertura de grilla** — cada celda (temperature, top-p) produce un conteo.
- **Profundidad de repetición** — 20 corridas revelan al menos tanta variación como 5.
- **Celda de prompt** — el barrido respeta el argumento de prompt por celda.

Los seis tests pasan offline con pytest 8.3 — el cliente mock hace la
variación determinista preservando la semántica de los parámetros.
