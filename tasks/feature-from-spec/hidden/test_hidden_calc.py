import pytest

from calc import evaluate


@pytest.mark.parametrize("expression, expected", [
    ("42", 42.0),
    ("4.5 * 2", 9.0),
    ("8 - 3 - 2", 3.0),
    ("8 / 4 / 2", 1.0),
    ("7 / 2", 3.5),
    ("((1 + 2) * (3 + 4))", 21.0),
    ("-3", -3.0),
    ("-(2 + 1)", -3.0),
    ("2 * -3", -6.0),
    ("2 * (3 + 4) - -1", 15.0),
    ("  1+2*3  ", 7.0),
])
def test_valid(expression, expected):
    result = evaluate(expression)
    assert isinstance(result, float)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize("expression", ["", "   ", "(1 + 2", "1 + 2)", "2 +", "3 4", "2 $ 3", "* 2"])
def test_invalid(expression):
    with pytest.raises(ValueError):
        evaluate(expression)


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate("1 / (2 - 2)")
