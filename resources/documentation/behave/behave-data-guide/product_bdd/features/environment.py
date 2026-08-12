"""Behave hooks that wire behave-data into the product catalog suite."""

from __future__ import annotations

import os
import re
from typing import Any

import behave_data.examples as _examples
from behave_data import (
    after_scenario_hook,
    before_feature_hook,
    before_scenario_hook,
    before_step_hook,
    register_type,
    setup_data,
)

from features.data import fixtures
from product_catalog import Catalog

# Behave stores tags without the leading '@', so match the tag name directly.
_examples._LOAD_TAG_PATTERN = re.compile(r"load_examples:(.*)")


def _parse_product_code(value: str) -> str:
    """Custom type: product codes must start with PRD-."""
    if not isinstance(value, str) or not value.startswith("PRD-"):
        raise ValueError(f"product code must start with PRD-, got {value!r}")
    return value


def before_all(context: Any) -> None:
    """Initialize behave-data, fixtures, builders, and secrets."""
    os.environ.setdefault("CATALOG_API_KEY", "test-key-12345")
    setup_data(context)
    register_type("product_code", _parse_product_code)
    fixtures.reset_builder_counter()


def before_feature(context: Any, feature: Any) -> None:
    """Load dynamic Examples from @load_examples tags."""
    before_feature_hook(context, feature)


def before_scenario(context: Any, scenario: Any) -> None:
    """Process declarative tags and reset per-scenario state."""
    before_scenario_hook(context, scenario)
    fixtures.reset_builder_counter()
    context.catalog = Catalog()


def before_step(context: Any, step: Any) -> None:
    """Resolve {placeholder} patterns in step tables."""
    before_step_hook(context, step)


def after_scenario(context: Any, scenario: Any) -> None:
    """Run cleanup registered by @cleanup_after."""
    after_scenario_hook(context, scenario)
