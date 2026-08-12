"""Fixtures and builders for the product catalog BDD suite."""

from __future__ import annotations

from datetime import date
from typing import Any

from behave_data import data_builder, data_fixture

_BUILDER_SEQ = 0


def reset_builder_counter() -> None:
    """Reset the builder product counter before each scenario."""
    global _BUILDER_SEQ
    _BUILDER_SEQ = 0


@data_fixture("regular_user", params=["alice", "bob"])
def regular_user(param: str) -> dict[str, Any]:
    """Return a parametrized user fixture."""
    return {
        "username": param,
        "email": f"{param}@qapractices.com",
        "role": "user",
    }


@data_fixture("admin_user")
def admin_user() -> dict[str, Any]:
    """Return an admin fixture that references a regular user."""
    return {
        "username": "admin",
        "email": "admin@qapractices.com",
        "role": "admin",
        "reports_to": "ref:regular_user:alice",
    }


def _parse_bool(value: Any) -> bool:
    """Parse a string or bool into a bool."""
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "yes", "1", "on"}


@data_builder("product")
def build_product(overrides: dict[str, Any]) -> dict[str, Any]:
    """Build a product dict with derived SKU and sensible defaults."""
    global _BUILDER_SEQ
    _BUILDER_SEQ += 1

    name = overrides.get("name", "Widget")
    sku = overrides.get("sku")
    if not sku:
        prefix = "".join(ch for ch in name if ch.isalnum())[:3].upper()
        sku = f"PRD-{prefix}-{_BUILDER_SEQ:03d}"

    return {
        "name": f"{name} #{_BUILDER_SEQ}",
        "sku": sku,
        "price": float(overrides.get("price", 9.99)),
        "active": _parse_bool(overrides.get("active", True)),
        "stock": int(overrides.get("stock", 10)),
        "released": overrides.get("released", date.today()),
        "description": overrides.get("description"),
    }
