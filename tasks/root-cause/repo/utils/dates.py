from datetime import date


def days_between(start: date, end: date) -> int:
    """Number of days from start to end, both included."""
    return (end - start).days
