from pagination import page_count, page

DATA = list(range(1, 11))


def test_first_page():
    assert page(DATA, 1, 4) == [1, 2, 3, 4]


def test_last_partial_page():
    assert page(DATA, 3, 4) == [9, 10]


def test_page_count_exact():
    assert page_count(DATA, 5) == 2


def test_page_count_partial():
    assert page_count(DATA, 4) == 3
