"""Minimal cart-to-order state machine used by the e-commerce checkout test cases.

Simulates the parts a QA cares about in TC-001..TC-016: cart math, coupon rules,
free-shipping thresholds, guest/registered paths, cart merge on login, idempotent
order placement and post-order state. Pure stdlib — no external services.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

FREE_SHIPPING_THRESHOLD = 50.0
STANDARD_SHIPPING = 4.99

# Stripe test card endings → simulated gateway response
CARD_RESULTS = {
    "4242424242424242": "succeeded",
    "4000000000000002": "card_declined",
    "4000000000009995": "insufficient_funds",
    "4000000000000069": "expired_card",
}


@dataclass
class Line:
    sku: str
    price: float
    qty: int


@dataclass
class Coupon:
    code: str
    amount: float
    min_subtotal: float = 0.0
    expired: bool = False


@dataclass
class Order:
    number: str
    email: str
    account: Optional[str]
    lines: list[Line]
    total: float
    status: str = "Processing"


@dataclass
class Cart:
    lines: dict[str, Line] = field(default_factory=dict)
    coupon: Optional[Coupon] = None

    def add(self, sku: str, price: float, qty: int = 1) -> None:
        if sku in self.lines:
            self.lines[sku].qty += qty
        else:
            self.lines[sku] = Line(sku, price, qty)

    def update_qty(self, sku: str, qty: int) -> None:
        self.lines[sku].qty = qty
        if qty <= 0:
            del self.lines[sku]

    def remove(self, sku: str) -> None:
        self.lines.pop(sku)

    def merge(self, other: "Cart") -> None:
        for line in other.lines.values():
            self.add(line.sku, line.price, line.qty)

    @property
    def item_count(self) -> int:
        return sum(line.qty for line in self.lines.values())

    @property
    def subtotal(self) -> float:
        return round(sum(l.price * l.qty for l in self.lines.values()), 2)

    @property
    def discount(self) -> float:
        if self.coupon and self.subtotal >= self.coupon.min_subtotal:
            return round(self.coupon.amount, 2)
        return 0.0

    @property
    def shipping(self) -> float:
        net = self.subtotal - self.discount
        return 0.0 if net >= FREE_SHIPPING_THRESHOLD else STANDARD_SHIPPING

    @property
    def total(self) -> float:
        return round(self.subtotal - self.discount + self.shipping, 2)

    def apply_coupon(self, coupon: Coupon) -> str:
        if coupon.expired:
            return "coupon expired"
        if self.subtotal < coupon.min_subtotal:
            return "minimum order amount not met"
        if self.coupon:
            return "one coupon per order"
        self.coupon = coupon
        return "applied"


class Store:
    """Simulates the storefront: carts, accounts, gateway and orders."""

    def __init__(self) -> None:
        self.accounts: dict[str, Cart] = {}
        self.orders: dict[str, Order] = {}
        self.emails_sent: list[dict] = []
        self._idempotency_keys: set[str] = set()
        self._order_seq = 12345

    def login(self, account: str) -> Cart:
        return self.accounts.setdefault(account, Cart())

    def merge_guest_cart(self, guest: Cart, account: str) -> Cart:
        self.login(account).merge(guest)
        return self.accounts[account]

    def place_order(
        self,
        cart: Cart,
        email: str,
        card: str,
        account: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> dict:
        """Place an order. Returns a Stripe-like response dict."""
        if idempotency_key and idempotency_key in self._idempotency_keys:
            return {"status_code": 200, "idempotent_replay": True}
        result = CARD_RESULTS.get(card, "succeeded")
        if result != "succeeded":
            return {
                "status_code": 402,
                "error": {"code": result if result == "card_declined" else "card_error",
                          "decline_code": result, "message": "Your card was declined."},
            }
        if idempotency_key:
            self._idempotency_keys.add(idempotency_key)
        self._order_seq += 1
        order = Order(
            number=f"ORD-{self._order_seq}",
            email=email,
            account=account,
            lines=list(cart.lines.values()),
            total=cart.total,
        )
        self.orders[order.number] = order
        self.emails_sent.append({
            "to": email,
            "subject": f"Your order {order.number} is confirmed",
            "items": [f"{l.sku} x{l.qty}" for l in order.lines],
            "total": order.total,
        })
        return {"status_code": 200, "order_number": order.number}

    def order_history(self, account: str) -> list[Order]:
        return [o for o in self.orders.values() if o.account == account]

    def guest_lookup(self, email: str, number: str) -> Optional[Order]:
        order = self.orders.get(number)
        if order and order.email == email:
            return order
        return None


def new_cart(**kwargs) -> Cart:
    return Cart(**kwargs)


def order_number() -> str:
    return f"ORD-{uuid.uuid4().int % 10**5}"
