"""TC-001..TC-016 mapped to executable asserts against checkout_flow.py."""

import pytest

from checkout_flow import (
    CARD_RESULTS,
    Cart,
    Coupon,
    Store,
    FREE_SHIPPING_THRESHOLD,
)


@pytest.fixture
def store():
    return Store()


# TC-001 — add item: badge, line, subtotal
def test_tc001_add_item_updates_cart():
    cart = Cart()
    cart.add("SKU-1001", 24.99, qty=2)
    assert cart.item_count == 2
    assert cart.lines["SKU-1001"].price == 24.99
    assert cart.subtotal == 49.98


# TC-002 — qty update recalculates
def test_tc002_update_quantity_recalculates():
    cart = Cart()
    cart.add("SKU-1001", 24.99)
    cart.update_qty("SKU-1001", 3)
    assert cart.subtotal == 74.97


# TC-003 — remove one line of several
def test_tc003_remove_item_updates_state():
    cart = Cart()
    for i in range(3):
        cart.add(f"SKU-100{i}", 10.00)
    cart.remove("SKU-1001")
    assert cart.item_count == 2
    assert "SKU-1001" not in cart.lines
    assert cart.subtotal == 20.00


# TC-004 — persistence is a serialize/restore concern; simulate via round-trip
def test_tc004_cart_state_serializable(store):
    cart = Cart()
    cart.add("SKU-1001", 24.99, qty=2)
    snapshot = {sku: (l.price, l.qty) for sku, l in cart.lines.items()}
    restored = Cart()
    for sku, (price, qty) in snapshot.items():
        restored.add(sku, price, qty)
    assert restored.subtotal == cart.subtotal


# TC-005 — valid fixed coupon
def test_tc005_valid_coupon_applies():
    cart = Cart()
    cart.add("SKU-1001", 50.00, qty=2)
    assert cart.apply_coupon(Coupon("SAVE20", 20.00, min_subtotal=20.0)) == "applied"
    assert cart.discount == 20.00
    # net 80 ≥ 50 threshold → free shipping
    assert cart.shipping == 0.0
    assert cart.total == 80.00


# TC-006 — invalid + stacking rejected
def test_tc006_invalid_and_stacking_coupons():
    cart = Cart()
    cart.add("SKU-1001", 50.00)
    assert cart.apply_coupon(Coupon("SAVE20", 20.0, min_subtotal=20.0)) == "applied"
    assert cart.apply_coupon(Coupon("EXTRA10", 10.0)) == "one coupon per order"
    small = Cart()
    small.add("SKU-2003", 15.00)
    assert small.apply_coupon(Coupon("SAVE20", 20.0, min_subtotal=20.0)) == "minimum order amount not met"


# TC-007 — guest checkout end-to-end
def test_tc007_guest_checkout(store):
    cart = Cart()
    cart.add("SKU-1001", 24.99)
    res = store.place_order(cart, "guest.qa@qapractices-test.dev", "4242424242424242")
    assert res["status_code"] == 200
    order = store.orders[res["order_number"]]
    assert order.account is None
    assert order.email == "guest.qa@qapractices-test.dev"


# TC-008 — registered checkout ties the order to the account
def test_tc008_registered_checkout(store):
    cart = store.login("qa_user_001")
    cart.add("SKU-1001", 24.99)
    res = store.place_order(cart, "qa@qapractices-test.dev", "4242424242424242", account="qa_user_001")
    assert store.orders[res["order_number"]].account == "qa_user_001"


# TC-009 — guest cart merges on login
def test_tc009_guest_cart_merges(store):
    guest = Cart()
    guest.add("SKU-1001", 24.99, qty=2)
    store.login("qa_user_001").add("SKU-2003", 9.99)
    merged = store.merge_guest_cart(guest, "qa_user_001")
    assert merged.item_count == 3
    assert merged.subtotal == 59.97


# TC-010 — free-shipping threshold crossing
def test_tc010_threshold_recalculates():
    cart = Cart()
    cart.add("SKU-1001", 49.99)
    assert cart.shipping == 4.99
    cart.add("SKU-2003", 1.50)
    assert cart.shipping == 0.0
    assert cart.subtotal >= FREE_SHIPPING_THRESHOLD


# TC-011 — idempotent place order
def test_tc011_double_submit_single_order(store):
    cart = Cart()
    cart.add("SKU-1001", 24.99)
    key = "ik-abc123"
    r1 = store.place_order(cart, "g@qapractices-test.dev", "4242424242424242", idempotency_key=key)
    r2 = store.place_order(cart, "g@qapractices-test.dev", "4242424242424242", idempotency_key=key)
    assert r1["status_code"] == 200 and r2["status_code"] == 200
    assert len(store.orders) == 1


# TC-012 — refresh mid-payment: replay does not double-charge
def test_tc012_refresh_replay_no_duplicate(store):
    cart = Cart()
    cart.add("SKU-1001", 24.99)
    key = "ik-retry"
    store.place_order(cart, "g@qapractices-test.dev", "4242424242424242", idempotency_key=key)
    store.place_order(cart, "g@qapractices-test.dev", "4242424242424242", idempotency_key=key)
    assert len(store.orders) == 1


# TC-013 — order carries confirmation essentials
def test_tc013_order_has_confirmation_fields(store):
    cart = Cart()
    cart.add("SKU-1001", 24.99)
    res = store.place_order(cart, "g@qapractices-test.dev", "4242424242424242")
    order = store.orders[res["order_number"]]
    assert order.number.startswith("ORD-")
    assert order.total == cart.total
    assert order.status == "Processing"


# TC-014 — confirmation email queued with contents
def test_tc014_confirmation_email(store):
    cart = Cart()
    cart.add("SKU-1001", 24.99)
    res = store.place_order(cart, "guest.qa@qapractices-test.dev", "4242424242424242")
    mail = store.emails_sent[-1]
    assert mail["to"] == "guest.qa@qapractices-test.dev"
    assert res["order_number"] in mail["subject"]
    assert mail["items"] == ["SKU-1001 x1"]


# TC-015 — order appears in account history
def test_tc015_order_in_history(store):
    cart = store.login("qa_user_001")
    cart.add("SKU-1001", 24.99)
    res = store.place_order(cart, "qa@qapractices-test.dev", "4242424242424242", account="qa_user_001")
    history = store.order_history("qa_user_001")
    assert history[0].number == res["order_number"]
    assert history[0].status == "Processing"


# TC-016 — guest lookup: right pair works, wrong email leaks nothing
def test_tc016_guest_lookup(store):
    cart = Cart()
    cart.add("SKU-1001", 24.99)
    res = store.place_order(cart, "guest.qa@qapractices-test.dev", "4242424242424242")
    assert store.guest_lookup("guest.qa@qapractices-test.dev", res["order_number"]) is not None
    assert store.guest_lookup("wrong@qapractices-test.dev", res["order_number"]) is None


# Bonus — decline path: 402 + preserved cart (mirrors the pytest snippet in the resource)
def test_declined_card_preserves_cart(store):
    cart = Cart()
    cart.add("SKU-1001", 24.99, qty=2)
    res = store.place_order(cart, "g@qapractices-test.dev", "4000000000000002")
    assert res["status_code"] == 402
    assert res["error"]["decline_code"] == "card_declined"
    assert cart.item_count == 2
    assert len(store.orders) == 0
