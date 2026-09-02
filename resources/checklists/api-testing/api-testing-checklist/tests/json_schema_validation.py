from jsonschema import validate

order_schema = {
    "type": "object",
    "properties": {
        "order_id": {"type": "string"},
        "status": {"enum": ["pending", "paid", "shipped"]},
        "total": {"type": "number", "minimum": 0}
    },
    "required": ["order_id", "status"]
}

def validate_order_response(response_json):
    validate(instance=response_json, schema=order_schema)
