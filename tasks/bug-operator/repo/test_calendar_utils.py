from calendar_utils import is_leap_year


def test_simple_leap_year():
    assert is_leap_year(2024)


def test_non_leap_year():
    assert not is_leap_year(2023)


def test_century():
    assert not is_leap_year(1900)


def test_century_multiple_of_400():
    assert is_leap_year(2000)
