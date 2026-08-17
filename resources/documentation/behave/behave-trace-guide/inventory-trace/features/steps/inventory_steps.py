from behave import given, when, then
from behave_trace import log

from inventory_service import InventoryService


@given('the product "{sku}" starts with {qty:d} units in stock')
def step_product_starts_with(context, sku, qty):
    context.service = InventoryService()
    context.service.set_stock(sku, qty)
    log(context, f"Stock initialized: {sku} = {qty}")


@when('a shipment adds {qty:d} units of "{sku}"')
def step_shipment_adds(context, qty, sku):
    context.service.increase(sku, qty)
    log(context, f"Shipment added: {qty} units of {sku}")


@when('an order removes {qty:d} units of "{sku}"')
def step_order_removes(context, qty, sku):
    context.service.decrease(sku, qty)
    log(context, f"Order removed: {qty} units of {sku}")


@then('the stock for "{sku}" should be {qty:d} units')
def step_stock_should_be(context, sku, qty):
    actual = context.service.get_stock(sku)
    assert actual == qty, f"Expected {qty} for {sku}, got {actual}"
