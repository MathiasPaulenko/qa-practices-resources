def calculate_total(items, discount=0.0):
    """Sum item price * qty, then apply a fractional discount (0.0-1.0)."""
    if not 0.0 <= discount <= 1.0:
        raise ValueError("Discount must be between 0 and 1")
    subtotal = sum(item["price"] * item["qty"] for item in items)
    return subtotal * (1 - discount)
