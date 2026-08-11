from behave import given, when, then
from behave_kit import (
    assert_soft,
    assert_soft_equals,
    load_data,
    TypedContext,
)
from catalog_service import Product, ProductCatalog, Cart


class CartSchema:
    catalog: ProductCatalog
    cart: Cart
    discount: float


@given('the product catalog contains "{name}" priced at {price:f}')
def step_catalog_contains(context, name, price):
    if not hasattr(context, 'typed'):
        context.typed = TypedContext(context, CartSchema)
        context.typed.setup(catalog=ProductCatalog(), cart=Cart(), discount=0.0)
    context.typed.catalog.add(Product(name, price))


@when('the user adds {quantity:d} {name} to the cart')
def step_user_adds(context, quantity, name):
    product = context.typed.catalog.find_by_name(name)
    context.typed.cart.add(product, quantity)


@when('a {discount:d}% voucher is applied')
def step_apply_voucher(context, discount):
    context.typed.discount = discount / 100.0


@then('the cart total should be {expected:f}')
def step_cart_total(context, expected):
    actual = context.typed.cart.total * (1 - context.typed.discount)
    assert_soft_equals(round(actual, 2), expected, "cart total mismatch")
    assert_soft(context.typed.discount >= 0, "discount should not be negative")


@given("the test users are loaded from CSV")
def step_load_users(context):
    context.users = load_data("tests/data/users.csv")


@then("there should be {count:d} users")
def step_user_count(context, count):
    assert len(context.users) == count
