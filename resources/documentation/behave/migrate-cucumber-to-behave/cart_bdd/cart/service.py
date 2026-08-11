from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Product:
    name: str
    price: float


@dataclass
class ProductCatalog:
    products: List[Product] = field(default_factory=list)

    def add(self, product: Product):
        self.products.append(product)

    def find_by_name(self, name: str) -> Optional[Product]:
        for product in self.products:
            if product.name == name:
                return product
        raise KeyError(f"Product {name} not found")


class Cart:
    def __init__(self):
        self.items: List[tuple[Product, int]] = []

    def add(self, product: Product, quantity: int):
        self.items.append((product, quantity))

    @property
    def total(self) -> float:
        return round(sum(product.price * quantity for product, quantity in self.items), 2)

    def clear(self):
        self.items.clear()
