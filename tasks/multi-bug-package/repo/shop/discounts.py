def apply_discount(amount: float, percent: int) -> float:
    """Apply a percentage discount (0 to 100) to an amount."""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return amount * (1 - percent // 100)
