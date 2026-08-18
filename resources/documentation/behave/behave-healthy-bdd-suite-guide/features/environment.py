"""Environment hooks for the shop BDD example."""

from shop import Cart, Catalog


def before_scenario(context, scenario):
    context.catalog = Catalog()
    context.cart = Cart(context.catalog)
