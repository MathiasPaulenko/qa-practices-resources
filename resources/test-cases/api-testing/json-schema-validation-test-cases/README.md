# JSON Schema Validation — Runnable Companion

Runnable companion for the [JSON Schema Validation Test Cases: Types, Required, Format](https://qapractices.com/test-cases/json-schema-validation-test-cases/) guide on QAPractices.

The fixture is the `order-create` schema used throughout the guide — an OrderService payload with required fields, nested `shippingAddress`/`$ref`/`$defs` resolution, `format: "email"`, enums, `minItems`/`maxItems`, `oneOf`/`anyOf`, `additionalProperties: false` and a conditional `if`/`then` for B2B orders. A pytest 8.3 suite exercises 20 of the guide's 30 cases against it with `jsonschema` 4.26, including the draft-2020-12 edge case where `format` is annotation-only without a `FormatChecker`.

## Contents

- `schemas/order-create.json` — the SchemaGuard order schema (draft 2020-12), with `$defs` for `address`, `geo` and the `oneOf` payment union
- `tests/test_order_schema_validation.py` — tests named `test_tc###_...` mapping 1:1 to the guide's TCs: type coercion, required fields, email format (with and without assertion), enum, array bounds, `additionalProperties`, `oneOf` exclusivity, broken `$ref`, nullable, string/number bounds, pattern, nested `$ref` chains, `if`/`then`, multi-error reporting and empty containers
- `tests/conftest.py` — schema loading plus two validators (with and without `FormatChecker`) to expose the annotation-only `format` edge
- `requirements.txt` — pytest 8.3 + jsonschema 4.26 (`[format]` extras for the format checkers)

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
pytest tests/ -v
```

All 44 tests should pass. The suite is deliberately paired: `test_tc013_invalid_email_rejected_with_format_assertion` fails the bad email only because a `FormatChecker` is registered, while `test_tc013_edge_format_is_annotation_only_without_checker` proves the same payload passes on a bare validator — the exact leak the guide warns about.

## What to try next

- Flip `additionalProperties` to `unevaluatedProperties` at the root and watch TC-017's behavior change around composed schemas.
- Compile the schema with `Draft7Validator` instead of `Draft202012Validator` to see how draft semantics shift.
- Mirror the same suite in JavaScript with Ajv 8.17 + `ajv-formats` — the guide's "Verify It Yourself" section has the starter snippet.
