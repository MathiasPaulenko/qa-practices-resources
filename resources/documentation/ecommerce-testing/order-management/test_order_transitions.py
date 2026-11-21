"""Order lifecycle test suite — pytest 8.3.4.

Run: pip install pytest==8.3.4 && pytest test_order_transitions.py -v
Covers: valid/invalid state transitions + payment idempotency invariant.
"""
import pytest

TRANSITIONS = {
    "pending": {"paid", "cancelled", "failed"},
    "paid": {"processing", "cancelled", "refunded"},
    "processing": {"shipped", "cancelled"},
    "shipped": {"delivered"},
    "delivered": {"refunded", "partially_refunded"},
    "partially_refunded": {"refunded"},
    "cancelled": set(),
    "failed": set(),
    "refunded": set(),
}

class OrderStateMachine:
    def __init__(self, state):
        self.state = state

    def transition(self, target):
        if target not in TRANSITIONS[self.state]:
            raise ValueError(f"Invalid transition: {self.state} -> {target}")
        self.state = target


@pytest.mark.parametrize("source,target", [
    ("pending", "paid"), ("paid", "processing"), ("processing", "shipped"),
    ("shipped", "delivered"), ("delivered", "refunded"),
])
def test_valid_transitions(source, target):
    order = OrderStateMachine(source)
    order.transition(target)
    assert order.state == target


@pytest.mark.parametrize("source,target", [
    ("pending", "shipped"), ("cancelled", "paid"), ("delivered", "processing"),
    ("refunded", "delivered"), ("shipped", "cancelled"),
])
def test_invalid_transitions_rejected(source, target):
    order = OrderStateMachine(source)
    with pytest.raises(ValueError):
        order.transition(target)
    assert order.state == source


class FakeGateway:
    def __init__(self):
        self.captures = {}

    def capture_count(self, key):
        return self.captures.get(key, 0)


class Order:
    def __init__(self, total_due):
        self.state = "pending"
        self.total_due = total_due
        self.total_captured = 0
        self.gateway = None

    def pay(self, idempotency_key):
        if self.gateway.capture_count(idempotency_key):
            return  # idempotent no-op on retry
        self.gateway.captures[idempotency_key] = 1
        self.total_captured = self.total_due
        self.state = "paid"


def test_payment_capture_is_idempotent():
    gateway = FakeGateway()
    order = Order(total_due=12990)
    order.gateway = gateway
    order.pay(idempotency_key="pay-42")
    order.pay(idempotency_key="pay-42")   # retry after timeout
    assert order.state == "paid"
    assert gateway.capture_count("pay-42") == 1
    assert order.total_captured == order.total_due
