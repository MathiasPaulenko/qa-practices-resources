"""In-memory product catalog for the behave-data example."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from typing import Any


@dataclass
class Product:
    """A product in the catalog."""

    name: str
    sku: str = ""
    price: float = 0.0
    active: bool = True
    stock: int = 0
    released: date | None = None
    description: str | None = None


class Catalog:
    """In-memory catalog that behaves-data scenarios exercise."""

    def __init__(self) -> None:
        self.products: list[Product] = []

    def clear(self) -> None:
        """Remove all products."""
        self.products = []

    def add(self, product: dict[str, Any]) -> Product:
        """Add a product from a dict and return the instance."""
        if "sku" not in product or not product["sku"]:
            product["sku"] = f"PRD-{product['name'][:3].upper()}"
        item = Product(**product)
        self.products.append(item)
        return item

    def as_dicts(self) -> list[dict[str, Any]]:
        """Return all products as plain dicts for diff."""
        return [asdict(p) for p in self.products]
