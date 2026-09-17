from behave import given, when, then


class Shop:
    def __init__(self):
        self.catalog = {}
        self.cart = {}

    def stock_product(self, name, price, units):
        self.catalog[name] = price

    def clear_cart(self):
        self.cart.clear()

    def add_to_cart(self, name):
        self.cart[name] = self.cart.get(name, 0) + 1

    def item_count(self):
        return sum(self.cart.values())

    def create_order(self, rows):
        self.cart.clear()
        for row in rows:
            self.cart[row["product"]] = self.cart.get(row["product"], 0) + int(row["quantity"])

    def total(self):
        return sum(self.catalog.get(name, 0) * qty for name, qty in self.cart.items())

    def total_formatted(self):
        return f"${self.total()}.00"


@given('I am logged in as a registered user')
def step_logged_in(context):
    context.shop = Shop()


@given('I have an empty shopping cart')
def step_empty_cart(context):
    context.shop.clear_cart()


@given('the following products exist:')
def step_products_exist(context):
    for row in context.table:
        context.shop.stock_product(row["name"], int(row["price"]), int(row["stock"]))


@when('I add "{name}" to the cart')
def step_add_item(context, name):
    context.shop.add_to_cart(name)


@when('I create an order with:')
def step_create_order(context):
    context.shop.create_order(context.table)


@then('the cart should contain {count:d} item')
def step_cart_count(context, count):
    assert context.shop.item_count() == count


@then('the cart total should be "{expected}"')
def step_cart_total(context, expected):
    assert context.shop.total_formatted() == expected


@then('the order total should be "{expected}"')
def step_order_total(context, expected):
    assert context.shop.total_formatted() == expected
