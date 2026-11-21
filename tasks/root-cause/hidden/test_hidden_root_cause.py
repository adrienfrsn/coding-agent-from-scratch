from datetime import date

from billing import prorated_amount
from leave import leave_days
from utils.dates import days_between


def test_days_between_same_day():
    assert days_between(date(2026, 1, 1), date(2026, 1, 1)) == 1


def test_days_between_across_months():
    assert days_between(date(2026, 1, 30), date(2026, 2, 2)) == 4


def test_leave_week():
    assert leave_days(date(2026, 3, 2), date(2026, 3, 6)) == 5


def test_billing_still_correct():
    assert prorated_amount(31.0, date(2026, 5, 1), date(2026, 5, 31), 31) == 31.0
