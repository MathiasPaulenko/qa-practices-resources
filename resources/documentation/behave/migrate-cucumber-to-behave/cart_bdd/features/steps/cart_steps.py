from behave import given, when, then
from cart.service import Product, ProductCatalog, Cart


@given('the product catalog contains "{name}" priced at {price:f}')
def step_catalog_contains(context, name, price):
    context.catalog.add(Product(name, price))


@when('the user adds {quantity:d} {name} to the cart')
def step_user_adds(context, quantity, name):
    product = context.catalog.find_by_name(name)
    context.cart.add(product, quantity)


@then('the cart total should be {expected:f}')
def step_cart_total(context, expected):
    assert context.cart.total == expected, f"Expected {expected}, got {context.cart.total}"
