from behave import given, when, then
from shop_domain import Product
from features.steps.shared import parse_money


@given('the catalog contains the following products:')
def step_catalog_table(context):
    for row in context.table:
        sku = row['SKU']
        price = parse_money(row['Price'])
        stock = int(row['Stock'])
        context.catalog[sku] = Product(
            sku=sku,
            name=row['Name'],
            unit_price=price,
            stock=stock,
        )


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
