from list_utils import first, last


def test_last():
    assert last([1, 2, 3, 4, 5], 2) == [4, 5]


def test_last_all():
    assert last([1, 2], 2) == [1, 2]


def test_first():
    assert first([1, 2, 3], 2) == [1, 2]
