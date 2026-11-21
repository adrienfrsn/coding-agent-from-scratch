from datetime import date

from billing import prorated_amount


def test_full_month():
    assert prorated_amount(30.0, date(2026, 4, 1), date(2026, 4, 30), 30) == 30.0


def test_half_month():
    assert prorated_amount(30.0, date(2026, 4, 1), date(2026, 4, 15), 30) == 15.0


def test_single_day():
    assert prorated_amount(30.0, date(2026, 4, 10), date(2026, 4, 10), 30) == 1.0
