# shop

Small shopping cart library.

- `shop/cart.py`: the `Cart` class, items are stored as `name -> (unit_price, quantity)`
- `shop/discounts.py`: percentage discounts
- `shop/pricing.py`: tax computation
- Tests live in `tests/`, run them from the project root with `python -m pytest -q`
- Amounts are floats rounded to 2 decimals
