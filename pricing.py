"""Order pricing, line item subtotals, and modifier charges."""


def order_total(items):
    """Calculate the menu subtotal including paid modifiers."""
    return round(sum(line["quantity"] * line["unit_price"] for line in items), 2)
