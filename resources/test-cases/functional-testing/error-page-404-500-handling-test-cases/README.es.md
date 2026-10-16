# Casos de Prueba de Páginas de Error (404, 500) — Companion Pytest

Código companion de [Casos de Prueba de Manejo de Páginas de Error (404, 500)](https://qapractices.com/es/test-cases/error-page-404-500-handling-test-cases/) en QAPractices.

## Qué hay dentro

| Archivo | Qué muestra |
|---------|-------------|
| `error_server.py` | Mock con `http.server` de stdlib que sirve páginas 404/403/413/429/500/503 personalizadas con códigos y headers correctos: negociación JSON 404, cadena de redirección que termina en 404, un bucle de redirección y dos rutas deliberadamente mal configuradas (`/misconfigured/404` soft 404, `/misconfigured/500-debug` fuga de stack trace y credenciales) para los casos negativos. |
| `tests/test_error_pages.py` | 15 casos pytest que cubren TC002, TC004, TC007, TC010, TC016, TC017, TC023, TC025, TC026, TC029, TC031, TC032, TC033 más los casos límite de cadena de redirección y header Server. |
| `tests/conftest.py` | Fixture de servidor con scope session en un puerto libre y reset del rate limit. |
| `requirements.txt` | `pytest==8.3.4`, `requests==2.32.3`. |

## Ejecutarlo

```bash
python -m venv .venv && .venv\Scripts\activate   # o source .venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -v
```

Esperado: **15 passed**.

La suite habla con `error_server.py` por loopback — no necesita servicios externos. Las rutas `/misconfigured/*` existen para demostrar los defectos; los tests que verifican el mal comportamiento documentan lo que TC016/TC017 atraparían en un sitio real.

## Recurso relacionado

- [Casos de Prueba de Manejo de Páginas de Error (404, 500)](https://qapractices.com/es/test-cases/error-page-404-500-handling-test-cases/) — la suite completa de 33 casos más la tabla edge/límite que este código automatiza.
