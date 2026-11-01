from slug import slugify


def test_simple():
    assert slugify("Hello World") == "hello-world"


def test_ponctuation():
    assert slugify("Salut, le monde !") == "salut-le-monde"


def test_espaces_multiples():
    assert slugify("  a   b  ") == "a-b"


def test_vide():
    assert slugify("") == ""
