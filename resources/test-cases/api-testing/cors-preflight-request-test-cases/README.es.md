# Casos de Prueba de CORS Preflight — Lab Companion

Companion de [Casos de Prueba de CORS Preflight: Headers y Métodos](https://qapractices.com/es/test-cases/cors-preflight-request-test-cases/) en QAPractices.

Un módulo de Python puro (stdlib) que modela los checks que hace el navegador
antes de un request cross-origin: si un request es "simple", el match exacto de
origin (esquema + host + puerto), los allow-lists de métodos/headers, la
violación de spec de credenciales con wildcard, el rechazo del origin `null` y
el cacheo con `Max-Age`.

## Estructura

```text
cors_preflight.py            — CorsConfig + evaluate_preflight + helpers
tests/test_cors_preflight.py — casos pytest mapeados a los TC-xxx del sitio
requirements.txt             — pytest 8.3.4
pytest.ini                   — testpaths/pythonpath
```

## Ejecutar

```bash
pip install -r requirements.txt
pytest -q
```

## Cobertura

Cada test mapea a un caso de prueba del sitio (TC001–TC030): requests simples,
preflights por JSON y headers custom, tupla de origin (subdominio, esquema,
puerto), violación wildcard+credenciales, `Origin: null`, `Authorization` en
allow-headers y cacheo con Max-Age.

El evaluador es determinista y offline — responde "¿el navegador dejaría pasar
esto?" dado un `CorsConfig` y un request, así que también sirve como lint para
cambios en la política CORS.
