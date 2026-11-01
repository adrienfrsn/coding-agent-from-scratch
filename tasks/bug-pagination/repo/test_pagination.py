from pagination import nombre_pages, page

DONNEES = list(range(1, 11))


def test_premiere_page():
    assert page(DONNEES, 1, 4) == [1, 2, 3, 4]


def test_derniere_page_partielle():
    assert page(DONNEES, 3, 4) == [9, 10]


def test_nombre_pages_exact():
    assert nombre_pages(DONNEES, 5) == 2


def test_nombre_pages_partiel():
    assert nombre_pages(DONNEES, 4) == 3
