"""Pytest suite mirroring the JSON Schema validation test cases on
qapractices.com/test-cases/json-schema-validation-test-cases/.

Each test names the TC-### it covers. jsonschema 4.26 + pytest 8.3.
"""

import pytest
from jsonschema.validators import validator_for


def keywords(errors):
    return {e.validator for e in errors}


def paths(errors):
    return {tuple(e.absolute_path) for e in errors}


# --- Positive cases -------------------------------------------------------

def test_tc001_tc003_tc007_valid_order_passes(validator, order):
    assert order  # sanity
    assert list(validator.iter_errors(order)) == []


def test_tc002_boolean_is_not_an_integer(validator, order):
    order["items"][0]["quantity"] = True
    errors = list(validator.iter_errors(order))
    assert keywords(errors) == {"type"}
    # jsonschema's integer check correctly excludes Python bool
    assert ("items", 0, "quantity") in paths(errors)


def test_tc005_enum_member_accepted(validator, order):
    order["priority"] = "express"
    assert list(validator.iter_errors(order)) == []


@pytest.mark.parametrize("size", [1, 25, 50])
def test_tc006_array_within_bounds(validator, order, size):
    order["items"] = [{"productId": f"PRD-{i}", "quantity": 1} for i in range(size)]
    assert list(validator.iter_errors(order)) == []


def test_tc008_oneof_exactly_one_branch(validator, order):
    order["payment"] = {"type": "credit_card", "cardNumber": "4111111111111111"}
    assert list(validator.iter_errors(order)) == []


@pytest.mark.parametrize("value", ["SAVE10", 15])
def test_tc009_anyof_accepts_either_branch(validator, order, value):
    order["discount"] = value
    assert list(validator.iter_errors(order)) == []


def test_tc010_local_ref_resolved(validator, order):
    order["shippingAddress"]["city"] = 123  # violation inside the $ref target
    errors = list(validator.iter_errors(order))
    assert keywords(errors) == {"type"}
    assert ("shippingAddress", "city") in paths(errors)


# --- Negative cases --------------------------------------------------------

def test_tc011_numeric_string_rejected_for_integer(validator, order):
    order["items"][0]["quantity"] = "2"
    errors = list(validator.iter_errors(order))
    assert keywords(errors) == {"type"}
    assert ("items", 0, "quantity") in paths(errors)


def test_tc012_missing_required_field(validator, order):
    del order["shippingAddress"]
    errors = list(validator.iter_errors(order))
    assert keywords(errors) == {"required"}
    assert "'shippingAddress' is a required property" in errors[0].message


def test_tc013_invalid_email_rejected_with_format_assertion(validator, order):
    order["contact"] = {"email": "not-an-email"}
    errors = list(validator.iter_errors(order))
    assert keywords(errors) == {"format"}


def test_tc013_edge_format_is_annotation_only_without_checker(bare_validator, order):
    order["contact"] = {"email": "not-an-email"}
    # Edge row: without FormatChecker, draft 2020-12 treats format as annotation.
    assert list(bare_validator.iter_errors(order)) == []


@pytest.mark.parametrize("bad_priority", ["urgent", "Express"])
def test_tc014_non_enum_value_rejected(validator, order, bad_priority):
    order["priority"] = bad_priority
    errors = list(validator.iter_errors(order))
    assert keywords(errors) == {"enum"}


def test_tc015_empty_items_array_rejected(validator, order):
    order["items"] = []
    assert keywords(list(validator.iter_errors(order))) == {"minItems"}


def test_tc016_items_above_maximum_rejected(validator, order):
    order["items"] = [{"productId": f"PRD-{i}", "quantity": 1} for i in range(51)]
    assert keywords(list(validator.iter_errors(order))) == {"maxItems"}


def test_tc017_unknown_field_rejected(validator, order):
    order["discountCode"] = "SAVE10"
    errors = list(validator.iter_errors(order))
    assert keywords(errors) == {"additionalProperties"}


def test_tc018_oneof_fails_when_two_branches_match(validator, order):
    # Loose schema: both branches accept the payload -> oneOf fails.
    loose = {
        "type": "object",
        "properties": {
            "payment": {
                "oneOf": [
                    {"properties": {"type": {"const": "credit_card"}}},
                    {"properties": {"type": {"const": "credit_card"}, "cardNumber": {"type": "string"}}},
                ]
            }
        },
    }
    v = validator_for(loose)(loose)
    errors = list(v.iter_errors({"payment": {"type": "credit_card", "cardNumber": "4111"}}))
    assert keywords(errors) == {"oneOf"}


def test_tc019_broken_ref_surfaces_as_resolution_error():
    # A dangling $ref is a schema bug, not a payload bug: jsonschema only
    # resolves it lazily, so the failure appears when the property is
    # evaluated — and it raises, it does not come back as `valid`.
    broken = {"type": "object", "properties": {"a": {"$ref": "#/$defs/missing"}}}
    v = validator_for(broken)(broken)
    with pytest.raises(Exception, match="does not exist"):
        list(v.iter_errors({"a": 1}))


def test_tc020_null_rejected_for_string(validator, order):
    order["customerId"] = None
    assert keywords(list(validator.iter_errors(order))) == {"type"}


# --- Edge / failure cases --------------------------------------------------

@pytest.mark.parametrize("value,ok", [("Enjoy!", True), (None, True), (42, False)])
def test_tc021_nullable_type_list(validator, order, value, ok):
    order["giftMessage"] = value
    errors = list(validator.iter_errors(order))
    assert (errors == []) is ok


@pytest.mark.parametrize(
    "coupon,ok", [("AB", False), ("ABC", True), ("SAVE10", True), ("X" * 20, True), ("X" * 21, False)]
)
def test_tc022_string_length_bounds(validator, order, coupon, ok):
    order["couponCode"] = coupon
    errors = list(validator.iter_errors(order))
    assert (errors == []) is ok


@pytest.mark.parametrize("points,ok", [(-1, False), (0, True), (10000, True), (10001, False)])
def test_tc023_number_range_bounds(validator, order, points, ok):
    order["loyaltyPoints"] = points
    errors = list(validator.iter_errors(order))
    assert (errors == []) is ok


@pytest.mark.parametrize(
    "phone,ok", [("+14155552671", True), ("0041155552671", False), ("call-me", False)]
)
def test_tc024_pattern_enforced(validator, order, phone, ok):
    order["phone"] = phone
    errors = list(validator.iter_errors(order))
    assert (errors == []) is ok


def test_tc025_nested_ref_chain_reports_inner_path(validator, order):
    order["shippingAddress"]["coordinates"] = {"lat": "40.7", "lng": -74.0}
    errors = list(validator.iter_errors(order))
    assert keywords(errors) == {"type"}
    assert ("shippingAddress", "coordinates", "lat") in paths(errors)


def test_tc026_items_schema_per_element(validator, order):
    order["items"].append({"productId": "PRD-999", "quantity": "two"})
    errors = list(validator.iter_errors(order))
    assert ("items", 1, "quantity") in paths(errors)


@pytest.mark.parametrize(
    "channel,tax,ok",
    [("b2b", "EU123456789", True), ("b2b", None, False), ("b2c", None, True)],
)
def test_tc027_tc028_allof_if_then(validator, order, channel, tax, ok):
    order["channel"] = channel
    if tax is not None:
        order["taxId"] = tax
    errors = list(validator.iter_errors(order))
    assert (errors == []) is ok


def test_tc029_all_violations_reported(validator, order):
    order["items"][0]["quantity"] = "2"
    del order["shippingAddress"]
    order["discountCode"] = "SAVE10"
    errors = list(validator.iter_errors(order))
    assert keywords(errors) == {"type", "required", "additionalProperties"}
    assert len(errors) == 3


def test_tc030_empty_object_ok_empty_array_rejected(validator, order):
    order["metadata"] = {}
    order["items"] = []
    errors = list(validator.iter_errors(order))
    assert keywords(errors) == {"minItems"}
