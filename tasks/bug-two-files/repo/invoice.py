from price import price_incl_vat


def total(lines):
    """lines: list of (price_excl_vat, quantity)."""
    return round(sum(price_incl_vat(p) * q for p, q in lines), 2)
