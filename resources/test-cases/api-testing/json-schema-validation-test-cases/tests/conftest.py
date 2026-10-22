import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "order-create.json"


@pytest.fixture(scope="session")
def schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def validator(schema):
    # FormatChecker is the opt-in that turns `format` into an assertion.
    return Draft202012Validator(schema, format_checker=FormatChecker())


@pytest.fixture(scope="session")
def bare_validator(schema):
    # No FormatChecker: under draft 2020-12 `format` is annotation-only here.
    return Draft202012Validator(schema)


@pytest.fixture()
def valid_order():
    return {
        "customerId": "CUST-8842",
        "items": [{"productId": "PRD-100", "quantity": 2}],
        "shippingAddress": {
            "street": "350 5th Ave",
            "city": "New York",
            "zipCode": "10118",
        },
    }


@pytest.fixture()
def order(valid_order):
    return copy.deepcopy(valid_order)
