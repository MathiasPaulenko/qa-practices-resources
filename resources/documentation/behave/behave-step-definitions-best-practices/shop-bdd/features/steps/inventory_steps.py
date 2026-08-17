from behave import given, when, then


@given('the product "{sku}" has a stock of {qty:d}')
def step_product_stock(context, sku, qty):
    if sku not in context.catalog:
        from shop_domain import Product
        context.catalog[sku] = Product(sku=sku, name=sku, unit_price=0, stock=0)
    context.catalog[sku].stock = qty
    context.inventory.set_stock(sku, qty)


@when('the stock alert threshold is {threshold:d}')
def step_alert_threshold(context, threshold):
    context.alert_threshold = threshold


@then('an alert should be sent for "{sku}"')
def step_alert_sent(context, sku):
    context.alert_service.check_low_stock(sku, context.alert_threshold)
    assert any(sku in alert for alert in context.alert_service.sent), f"No alert for {sku}"
