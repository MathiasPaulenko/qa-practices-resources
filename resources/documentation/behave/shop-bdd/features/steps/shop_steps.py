# features/steps/shop_steps.py
from behave import given, when, then, register_type
from shop_domain import Product
import parse


@parse.with_pattern(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?')
def parse_money(text):
    return int(round(float(text.replace('$', '').replace(',', '')) * 100))


@parse.with_pattern(r'\d+%')
def parse_percentage(text):
    return int(text.replace('%', ''))


register_type(Money=parse_money, Percentage=parse_percentage)


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


@given('the catalog contains the following products:')
def step_catalog_products(context):
    for row in context.table:
        sku = row['SKU']
        name = row['Name']
        price = parse_money(row['Price'])
        stock = int(row['Stock'])
        context.catalog[sku] = Product(sku=sku, name=name, unit_price=price, stock=stock)


@when('a customer searches for "{name}"')
def step_search_product(context, name):
    context.search_results = [
        p for p in context.catalog.values()
        if name.lower() in p.name.lower()
    ]


@then('the search results should contain {count:d} {label}')
def step_search_count(context, count, label):
    actual = len(context.search_results)
    assert actual == count, f'Expected {count} {label}, found {actual}'


@then('the first result should be "{sku}"')
def step_first_result(context, sku):
    assert context.search_results[0].sku == sku


@given('the warehouse has the following stock levels:')
def step_warehouse_stock(context):
    for row in context.table:
        context.inventory.set_stock(row['SKU'], int(row['Quantity']))


@when('the system checks stock for "{sku}" with threshold {threshold:d}')
def step_check_stock(context, sku, threshold):
    context.alert_service.check_low_stock(sku, threshold)


@then('a low stock alert should be sent for "{sku}"')
def step_alert_sent(context, sku):
    expected = f'LOW_STOCK:{sku}:{context.inventory.level(sku)}'
    assert expected in context.alert_service.sent, context.alert_service.sent


@then('no low stock alert should be sent')
def step_no_alert(context):
    assert not context.alert_service.sent


@given('the customer has spent {lifetime_spend:Money} in the last year')
def step_customer_spent(context, lifetime_spend):
    context.lifetime_spend = lifetime_spend


@when('the customer checks their tier discount')
def step_check_tier(context):
    context.tier = context.loyalty.tier_for(context.lifetime_spend)
    context.tier_discount = context.loyalty.discount(context.lifetime_spend)


@then('the discount should be {expected:Percentage}')
def step_tier_discount(context, expected):
    assert context.tier_discount == expected


@then('the tier name should be {expected}')
def step_tier_name(context, expected):
    assert context.tier == expected
