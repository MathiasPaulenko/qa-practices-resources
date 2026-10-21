# Casos de Prueba de Detección de Alucinaciones — Companion

Recurso complementario de [Detección de Alucinaciones: 20 Casos de Prueba](https://qapractices.com/es/test-cases/hallucination-detection-test-cases/).

## Contenido

- `claim_verifier.py` — modelo solo-stdlib del pipeline de detección: `extract_claims` divide la salida generada en oraciones atómicas, `verify_claim` verifica cada afirmación contra las fuentes recuperadas (la cobertura de tokens sustituye la llamada de embeddings/NLI del artículo, así todo corre offline), y `verify` puntúa soportadas/total y devuelve una decisión ship/review. `Verdict` distingue `SUPPORTED`, `UNSUPPORTED` y `CONTRADICTED` — esta última cubre conflictos numéricos y fuentes que discrepan.
- `tests/conftest.py` — pone el motor en `sys.path`.
- `tests/test_claim_verifier.py` — subconjunto ejecutable de los casos del artículo: persona inexistente (TC-01), año de fundación inexistente (TC-02), estadística sin respaldo (TC-03), evento post-corte (TC-04), cita fabricada (TC-05), contradicción numérica (TC-06), memoria paramétrica (TC-07), elemento de lista inventado (TC-09), definición de término de dominio (TC-10), inferencia de relación (TC-12), geografía no declarada (TC-13), fuentes conflictivas (TC-16), conjunto de fuentes vacío (TC-17) y contexto mínimo (TC-18).

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Salida esperada: `17 passed`.

El verificador es deliberadamente solo-stdlib. En producción cambia `_coverage` por similitud coseno de embeddings (sentence-transformers) o un cross-encoder NLI como `cross-encoder/nli-deberta-v3-large`, como describe el artículo.

## Relacionados

- Artículo EN: https://qapractices.com/test-cases/hallucination-detection-test-cases/
- Artículo ES: https://qapractices.com/es/test-cases/hallucination-detection-test-cases/
