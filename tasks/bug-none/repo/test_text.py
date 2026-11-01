from text import clean


def test_clean():
    assert clean("  Hello ") == "hello"


def test_clean_none():
    assert clean(None) == ""
