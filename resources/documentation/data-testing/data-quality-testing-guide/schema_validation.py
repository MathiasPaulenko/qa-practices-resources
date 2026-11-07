"""Schema validation example from the Data Quality Guide.

https://qapractices.com/documentation/data-quality-testing-guide/

Requires: pip install jsonschema
Tested with: Python 3.11, jsonschema 4.x
"""

from jsonschema import validate
from jsonschema.exceptions import ValidationError

schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "integer", "minimum": 1},
        "email": {"type": "string", "format": "email"},
        "signup_date": {"type": "string", "format": "date"},
    },
    "required": ["user_id", "email"],
}


def validate_record(record: dict) -> bool:
    """Validate one incoming record against the schema.

    Returns True when valid; raises ValidationError with the offending
    field when invalid — wire that into your ingestion gate.
    """
    validate(record, schema)
    return True


if __name__ == "__main__":
    good = {"user_id": 42, "email": "ana@qapractices.dev", "signup_date": "2026-11-07"}
    bad = {"user_id": 0, "signup_date": "not-a-date"}  # missing email + bad types

    print("valid record:", validate_record(good))
    try:
        validate_record(bad)
    except ValidationError as exc:
        print("invalid record rejected:", exc.message)
