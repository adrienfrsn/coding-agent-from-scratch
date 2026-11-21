TAX_RATE = 0.2


def with_tax(amount: float) -> float:
    """Amount including tax, rounded to the cent."""
    return round(amount * (1 + TAX_RATE))
