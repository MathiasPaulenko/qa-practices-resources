"""Step definitions for the product catalog data scenarios."""

from __future__ import annotations

from typing import Any

from behave import given, then, when
from behave_data import diff, register_type, typed_wrap

# Ensure fixtures and builders are registered before they are used.
from features.data import fixtures


def _parse_product_code(value: str) -> str:
    """Custom type: product codes must start with PRD-."""
    if not isinstance(value, str) or not value.startswith("PRD-"):
        raise ValueError(f"product code must start with PRD-, got {value!r}")
    return value


register_type("product_code", _parse_product_code)


class _TypedTable:
    """A minimal table-like object with clean headings and typed rows."""

    def __init__(self, headings: list[str], rows: list[dict[str, Any]]) -> None:
        self.headings = headings
        self.rows = rows


def _as_typed_table(table: Any, context: Any) -> _TypedTable:
    """Return a table-like object that diff() can compare against typed data."""
    wrapped = typed_wrap(table, context.data.config)
    return _TypedTable(wrapped.clean_headers(), wrapped.typed_dicts())


@given('the catalog is empty')
def step_catalog_empty(context: Any) -> None:
    """Reset the catalog before a scenario that needs a clean state."""
    context.catalog.clear()


@when('I add the following products')
def step_add_products(context: Any) -> None:
    """Add products from a typed Gherkin table to the catalog."""
    for product in typed_wrap(context.table, context.data.config).typed_dicts():
        context.catalog.add(product)


@then('the catalog should contain the following products')
def step_match_products(context: Any) -> None:
    """Compare the catalog against the expected typed table."""
    expected = _as_typed_table(context.table, context)
    actual = context.catalog.as_dicts()
    diff(expected, actual, ordered=False, surplus_columns=False)


@when('I import a product with name "{name}", price {price}, active "{active}" and stock {stock}')
def step_import_product(context: Any, name: str, price: str, active: str, stock: str) -> None:
    """Import a product from a scenario outline row with primitive conversion."""
    product = {
        "name": name,
        "price": float(price),
        "active": active.lower() == "true",
        "stock": int(stock),
    }
    context.catalog.add(product)


@then('the catalog should contain the product "{name}"')
def step_contains_product(context: Any, name: str) -> None:
    """Assert the catalog contains a product by name."""
    assert any(p["name"] == name for p in context.catalog.as_dicts())


@when('I import a price tier "{tier}" with sku "{sku}" and price {price}')
def step_import_price(context: Any, tier: str, sku: str, price: str) -> None:
    """Import a product from the JSON price list."""
    product = {
        "name": sku,
        "price": float(price),
        "active": True,
        "stock": 0,
    }
    context.catalog.add(product)


@when('I build {count:d} "{builder_name}" items with name prefix "{name_prefix}"')
def step_build_products(context: Any, count: int, builder_name: str, name_prefix: str) -> None:
    """Use the product builder to generate items and add them to the catalog."""
    products = context.data.build(
        builder_name, overrides={"name": name_prefix}, count=count
    )
    if not isinstance(products, list):
        products = [products]
    for product in products:
        context.catalog.add(product)


@then('the catalog should contain {count:d} products with name starting with "{prefix}"')
def step_check_built_products(context: Any, count: int, prefix: str) -> None:
    """Assert that the builder produced the expected count and name prefix."""
    assert len(context.catalog.as_dicts()) == count
    for product in context.catalog.as_dicts():
        assert product["name"].startswith(prefix)


@given('a registered user "{username}" with email "{email}" and role "{role}"')
def step_load_user(context: Any, username: str, email: str, role: str) -> None:
    """Load a parametrized fixture and verify CSV values."""
    user = context.data.fixture(f"regular_user:{username}")
    assert user["email"] == email
    assert user["role"] == role
    context.user = user


@then('the loaded user matches the fixture')
def step_user_matches_fixture(context: Any) -> None:
    """Confirm the CSV-loaded user is the same as the fixture."""
    assert context.user is not None
    assert context.user["username"] in {"alice", "bob"}


@then('the loaded user has username "{username}" and role "{role}"')
def step_check_tag_user(context: Any, username: str, role: str) -> None:
    """Verify a user loaded through @needs_data or @with_fixture tags."""
    user = getattr(context, f"regular_user:{username}")
    assert user["username"] == username
    assert user["role"] == role


@then('the admin has username "{username}" and reports to user "{report}"')
def step_check_admin(context: Any, username: str, report: str) -> None:
    """Verify the nested admin fixture resolved its ref: reference."""
    admin = getattr(context, "admin_user")
    assert admin["username"] == username
    assert admin["reports_to"]["username"] == report


@when('I resolve the API key from env')
def step_resolve_secret(context: Any) -> None:
    """Resolve a secret placeholder using the env backend."""
    context.resolved_key = context.data.resolve("secret:CATALOG_API_KEY")


@then('the resolved value is masked in logs')
def step_mask_secret(context: Any) -> None:
    """Assert that resolved secret values are masked by DataManager."""
    assert context.resolved_key is not None
    assert context.data.mask(context.resolved_key) == "***"
