"""Tiny in-memory checkout and inventory service for the behave-pool example."""

from __future__ import annotations


class Inventory:
    """Simple in-memory inventory."""

    def __init__(self) -> None:
        self.stock: dict[str, int] = {}

    def add(self, sku: str, quantity: int) -> None:
        self.stock[sku] = quantity

    def reserve(self, sku: str, quantity: int) -> None:
        if sku not in self.stock:
            raise ValueError(f"SKU {sku} not found")
        if self.stock[sku] < quantity:
            raise ValueError(f"Not enough stock for {sku}")
        self.stock[sku] -= quantity

    def quantity(self, sku: str) -> int:
        return self.stock.get(sku, 0)


class Cart:
    """Simple in-memory shopping cart."""

    def __init__(self) -> None:
        self.items: dict[str, float] = {}

    def add(self, sku: str, price: float) -> None:
        self.items[sku] = price

    def total(self) -> float:
        return round(sum(self.items.values()), 2)


class PaymentGateway:
    """Simulated rate-limited payment gateway."""

    def __init__(self) -> None:
        self._charged = False

    def charge(self, amount: float) -> bool:
        if self._charged:
            raise RuntimeError("Gateway already charged in this process")
        if amount <= 0:
            return False
        self._charged = True
        return True
