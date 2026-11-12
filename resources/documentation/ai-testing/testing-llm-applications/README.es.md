# Companion de Testing de Aplicaciones con LLM

Recurso complementario de [Testing de Aplicaciones con LLM](https://qapractices.com/es/documentation/testing-llm-applications). Suite pytest ejecutable que implementa las cuatro capas de validación de la guía: contrato de esquema, similitud semántica, probes de inyección adversariales y regresión con golden dataset.

## Archivos

| Archivo | Capa | Qué hace | Stack |
|---------|------|----------|-------|
| `support_bot.py` | — | Stub determinístico de un endpoint LLM — reemplazá `ask()` con tu cliente real | Python 3.9+ |
| `test_schema.py` | 1 | Valida la forma de la respuesta y el contrato de citas | jsonschema 4.22+ |
| `test_semantic.py` | 2 | Piso de similitud de embeddings vs respuesta esperada | sentence-transformers, all-MiniLM-L6-v2 |
| `test_injection.py` | 3 | Probes OWASP LLM01 parametrizados | pytest 8.x |
| `test_golden_regression.py` + `golden_dataset.jsonl` | 4 | Evalúa preguntas reales contra keywords obligatorios | pytest 8.x |

## Quick Start

```bash
pip install pytest jsonschema numpy sentence-transformers
pytest -v

# Capas que corren sin descargar el modelo de embeddings:
pytest test_schema.py test_injection.py test_golden_regression.py -v
```

El stub hace que todas las capas corran offline — apuntá `ask()` a tu endpoint real y los mismos tests aplican.

## Requisitos

- Python 3.9+
- `pytest`, `jsonschema` para capas 1, 3 y 4
- `sentence-transformers` + `numpy` para capa 2 (el modelo descarga ~90MB una vez)
