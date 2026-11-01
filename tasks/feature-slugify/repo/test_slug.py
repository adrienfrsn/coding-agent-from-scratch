from slug import slugify


def test_simple():
    assert slugify("Hello World") == "hello-world"


def test_punctuation():
    assert slugify("Hi, big world !") == "hi-big-world"


def test_multiple_spaces():
    assert slugify("  a   b  ") == "a-b"


def test_empty():
    assert slugify("") == ""
