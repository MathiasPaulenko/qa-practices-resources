from behave import given, register_type
from parse import with_pattern


@with_pattern(r"\d+\.\d{2}")
def parse_price(text):
    return float(text)


register_type(Price=parse_price)


@given('the catalog contains "{title}" priced at "${price:Price}"')
def step_catalog_contains(context, title, price):
    context.catalog.add(title, price, stock=10)
