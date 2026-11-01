from helpers import add_1, add_60, percentile


def test_add():
    assert add_1(1) == 2
    assert add_60(1) == 61


def test_percentile_median():
    assert percentile([1, 2, 3, 4, 5], 50) == 3


def test_percentile_max():
    assert percentile([1, 2, 3, 4, 5], 100) == 5


def test_percentile_min():
    assert percentile([1, 2, 3, 4, 5], 0) == 1
