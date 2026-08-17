# shop_domain.py
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class Product:
    sku: str
    name: str
    unit_price: int
    stock: int = 0


@dataclass
class Cart:
    items: List[Tuple[Product, int]] = field(default_factory=list)

    def add(self, product: Product, quantity: int = 1):
        if product.stock < quantity:
            raise OutOfStockError(product.sku, quantity, product.stock)
        product.stock -= quantity
        self.items.append((product, quantity))

    def total(self, discount_engine: Optional['DiscountEngine'] = None) -> int:
        total = 0
        for product, qty in self.items:
            discount = discount_engine.discount_for(product.sku, qty) if discount_engine else 0
            total += product.unit_price * qty * (100 - discount) // 100
        return total


class OutOfStockError(Exception):
    def __init__(self, sku, requested, available):
        self.sku = sku
        self.requested = requested
        self.available = available


class DiscountEngine:
    def __init__(self, rules: Optional[List[Tuple[str, int, int]]] = None):
        self.rules = rules or []

    def discount_for(self, sku: str, quantity: int) -> int:
        for rule_sku, min_qty, percentage in self.rules:
            if rule_sku == sku and quantity >= min_qty:
                return percentage
        return 0


class LoyaltyProgram:
    TIERS = {
        'bronze': {'threshold': 0, 'discount': 0},
        'silver': {'threshold': 500000, 'discount': 5},
        'gold': {'threshold': 1500000, 'discount': 10},
    }

    def tier_for(self, lifetime_spend_cents: int) -> str:
        matched = 'bronze'
        for tier, data in self.TIERS.items():
            if lifetime_spend_cents >= data['threshold'] and data['threshold'] >= self.TIERS[matched]['threshold']:
                matched = tier
        return matched

    def discount(self, lifetime_spend_cents: int) -> int:
        return self.TIERS[self.tier_for(lifetime_spend_cents)]['discount']


class Inventory:
    def __init__(self, items: Optional[dict] = None):
        self.items = items or {}

    def set_stock(self, sku: str, quantity: int):
        self.items[sku] = quantity

    def level(self, sku: str) -> int:
        return self.items.get(sku, 0)

    def is_low(self, sku: str, threshold: int = 10) -> bool:
        return self.level(sku) <= threshold

    def reserve(self, sku: str, quantity: int):
        if self.level(sku) < quantity:
            raise OutOfStockError(sku, quantity, self.level(sku))
        self.items[sku] -= quantity


class AlertService:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory
        self.sent: List[str] = []

    def check_low_stock(self, sku: str, threshold: int = 10):
        if self.inventory.is_low(sku, threshold):
            self.sent.append(f'LOW_STOCK:{sku}:{self.inventory.level(sku)}')
