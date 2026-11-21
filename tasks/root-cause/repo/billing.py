from datetime import date

from utils.dates import days_between


def prorated_amount(monthly_price: float, start: date, end: date, days_in_month: int) -> float:
    """Price of a subscription active from start to end (both included)."""
    return round(monthly_price * days_between(start, end) / days_in_month, 2)
