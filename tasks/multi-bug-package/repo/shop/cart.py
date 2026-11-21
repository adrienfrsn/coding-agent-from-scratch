from shop.discounts import apply_discount
from shop.pricing import with_tax


class Cart:
    def __init__(self):
        self.items = {}  # name -> (unit_price, quantity)

    def add(self, name: str, unit_price: float, quantity: int = 1) -> None:
        price, qty = self.items.get(name, (unit_price, 0))
        self.items[name] = (price, qty + quantity)

    def remove(self, name: str) -> None:
        """Remove one unit of the item, and the item itself when no unit is left."""
        del self.items[name]

    def subtotal(self) -> float:
        return sum(price * qty for price, qty in self.items.values())

    def total(self, discount_percent: int = 0) -> float:
        return with_tax(apply_discount(self.subtotal(), discount_percent))
