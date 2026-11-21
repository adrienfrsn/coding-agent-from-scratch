from calc import evaluate


def test_addition():
    assert evaluate("1 + 2") == 3.0


def test_precedence():
    assert evaluate("2 + 3 * 4") == 14.0


def test_parentheses():
    assert evaluate("(2 + 3) * 4") == 20.0
