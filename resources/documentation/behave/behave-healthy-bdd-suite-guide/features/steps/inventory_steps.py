from behave import when, then


@when('the customer checks stock for "{title}"')
def step_check_stock(context, title):
    context.checked_stock = context.catalog.stock(title)


@then('the stock count should be {stock:d}')
def step_stock_count(context, stock):
    assert context.checked_stock == stock, (
        f"Expected stock {stock}, got {context.checked_stock}"
    )
