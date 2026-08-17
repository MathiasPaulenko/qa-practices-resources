from behave import given, when, then
from shop_domain import Product
from features.steps.shared import *  # registers Money, Percentage


@given('the product "{sku}" costs {price:Money}')
def step_product_costs(context, sku, price):
    context.catalog[sku] = Product(sku=sku, name=sku, unit_price=price, stock=100)


@given('the catalog has a bulk discount of {discount:Percentage} for at least {min_qty:d} of "{sku}"')
def step_bulk_discount(context, discount, min_qty, sku):
    context.discount_engine.rules.append((sku, min_qty, discount))


@when('a customer adds {qty:d} of "{sku}" to the cart')
def step_add_to_cart(context, qty, sku):
    product = context.catalog[sku]
    context.cart.add(product, qty)


@then('the cart total should be {expected:Money}')
def step_cart_total(context, expected):
    actual = context.cart.total(context.discount_engine)
    assert actual == expected, f'Expected ${expected/100:.2f}, got ${actual/100:.2f}'
