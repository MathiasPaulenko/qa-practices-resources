# Validación JSON Schema — Companion Ejecutable

Companion ejecutable de la guía [Casos de Prueba de Validación JSON Schema: Tipos, Required y Format](https://qapractices.com/es/test-cases/json-schema-validation-test-cases/) de QAPractices.

El fixture es el esquema `order-create` usado en toda la guía — un payload de OrderService con campos requeridos, resolución anidada `shippingAddress`/`$ref`/`$defs`, `format: "email"`, enums, `minItems`/`maxItems`, `oneOf`/`anyOf`, `additionalProperties: false` y un condicional `if`/`then` para órdenes B2B. Una suite pytest 8.3 ejercita 20 de los 30 casos de la guía contra él con `jsonschema` 4.26, incluido el edge case de draft 2020-12 donde `format` es solo anotación sin `FormatChecker`.

## Contenido

- `schemas/order-create.json` — el esquema de orden de SchemaGuard (draft 2020-12), con `$defs` para `address`, `geo` y la unión `oneOf` de pago
- `tests/test_order_schema_validation.py` — tests nombrados `test_tc###_...` mapeados 1:1 con los TCs de la guía: coerción de tipos, campos requeridos, formato email (con y sin aserción), enum, límites de array, `additionalProperties`, exclusividad de `oneOf`, `$ref` roto, nullable, límites de string/number, pattern, cadenas `$ref` anidadas, `if`/`then`, reporte multi-error y contenedores vacíos
- `tests/conftest.py` — carga del esquema y dos validadores (con y sin `FormatChecker`) para exponer el borde de `format` como anotación
- `requirements.txt` — pytest 8.3 + jsonschema 4.26 (extras `[format]` para los checkers de formato)

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Los 44 tests deberían pasar. La suite está emparejada a propósito: `test_tc013_invalid_email_rejected_with_format_assertion` rechaza el email malo solo porque hay un `FormatChecker` registrado, mientras `test_tc013_edge_format_is_annotation_only_without_checker` demuestra que el mismo payload pasa en un validador pelado — justo la fuga que advierte la guía.

## Qué probar después

- Cambia `additionalProperties` por `unevaluatedProperties` en la raíz y observa cómo cambia el comportamiento del TC-017 con esquemas compuestos.
- Compila el esquema con `Draft7Validator` en lugar de `Draft202012Validator` para ver cómo cambia la semántica entre drafts.
- Replica la misma suite en JavaScript con Ajv 8.17 + `ajv-formats` — la sección "Verifícalo Tú Mismo" de la guía tiene el snippet inicial.
