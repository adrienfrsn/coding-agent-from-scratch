import pytest

from shop.cart import Cart
from shop.discounts import apply_discount
from shop.pricing import with_tax


def make_cart():
    cart = Cart()
    cart.add("pen", 1.5, 2)
    cart.add("book", 12.0)
    return cart


def test_subtotal():
    assert make_cart().subtotal() == 15.0


def test_remove_one_unit():
    cart = make_cart()
    cart.remove("pen")
    assert cart.items["pen"] == (1.5, 1)


def test_remove_last_unit():
    cart = make_cart()
    cart.remove("book")
    assert "book" not in cart.items


def test_discount():
    assert apply_discount(100.0, 15) == pytest.approx(85.0)


def test_discount_invalid():
    with pytest.raises(ValueError):
        apply_discount(10.0, 120)


def test_with_tax():
    assert with_tax(10.99) == 13.19


def test_total_with_discount():
    assert make_cart().total(10) == 16.2
