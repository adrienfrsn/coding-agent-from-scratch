from config import VAT, LOYALTY_DISCOUNT


def price_incl_vat(price_excl_vat):
    return round(price_excl_vat * (1 + VAT), 2)


def loyalty_price(price_excl_vat):
    return price_incl_vat(price_excl_vat * (1 - LOYALTY_DISCOUNT))
