from datetime import date

from utils.dates import days_between


def leave_days(start: date, end: date) -> int:
    """Number of calendar days of a leave, first and last day included."""
    return days_between(start, end)
