# Casos de Prueba de SQL Injection — Lab Companion

Lab ejecutable para el recurso [Casos de Prueba de SQL Injection](https://qapractices.com/es/test-cases/sql-injection-test-cases/) de QAPractices.

Una app mínima Flask + SQLite expone las mismas funciones dos veces: los endpoints `/vulnerable/*` construyen SQL por concatenación de strings (intencionalmente inyectables), y los `/secure/*` usan queries parametrizadas. La suite pytest dispara los payloads del recurso contra ambos y verifica la diferencia observable — esto es cómo se ve "resultado esperado: vulnerable vs seguro" cuando se ejecuta de verdad.

## Requisitos

- Python 3.10+
- `pip install -r requirements.txt`

## Ejecutar

```bash
pytest -v
```

Esperado: todos los tests pasan. Cada test documenta el comportamiento vulnerable *y* el protegido — la suite está verde porque ambos lados se comportan como fue diseñado.

## Qué verifica cada test

| Test | Corresponde a | Demuestra |
|---|---|---|
| `test_normal_login_works_on_both_endpoints` | Baseline | Ambos formularios de login aceptan credenciales reales |
| `test_vulnerable_login_bypassed_by_classic_payload` | TC-SQLI-001 | `' OR '1'='1'--` hace login como `admin` sin contraseña |
| `test_vulnerable_login_naive_payload_does_not_bypass` | TC-SQLI-001 | El `' OR '1'='1` pelado falla — `AND` liga más fuerte que `OR`, así que el check de contraseña igual se exige |
| `test_secure_login_treats_payload_as_literal` | TC-SQLI-001 | Payload → HTTP 401, tratado como string literal |
| `test_vulnerable_search_allows_union_exfiltration` | TC-SQLI-002 | El payload UNION filtra usernames + hashes de contraseña en los resultados |
| `test_secure_search_treats_union_as_literal` | TC-SQLI-002 | El mismo payload → conjunto vacío |
| `test_vulnerable_numeric_param_returns_all_rows` | Tabla edge | `id=1 OR 1=1` devuelve la tabla products completa |
| `test_secure_numeric_param_rejects_expression` | Tabla edge | El mismo input → sin filas |

## Notas

- La base de datos es en memoria y se siembra al importar — sin setup, sin estado entre corridas.
- `pytest.ini` define `pythonpath = .` para que los tests importen `app.py` directamente.
- El código vulnerable existe solo para entrenamiento. Nunca publiques queries concatenadas — los endpoints `/secure/*` muestran el patrón correcto.
