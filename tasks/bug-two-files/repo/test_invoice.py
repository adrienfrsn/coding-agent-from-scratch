from invoice import total
from price import price_incl_vat, loyalty_price


def test_price_incl_vat():
    assert price_incl_vat(100) == 120


def test_loyalty_price():
    assert loyalty_price(100) == 114


def test_total():
    assert total([(100, 2), (50, 1)]) == 300
