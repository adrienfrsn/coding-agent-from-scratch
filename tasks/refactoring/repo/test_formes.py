import math

import pytest

from formes import aire_carre, aire_cercle, aire_rectangle


def test_aires():
    assert aire_carre(3) == 9
    assert aire_rectangle(2, 5) == 10
    assert aire_cercle(1) == pytest.approx(math.pi)


@pytest.mark.parametrize("appel", [
    lambda: aire_carre(-1),
    lambda: aire_cercle(-1),
    lambda: aire_rectangle(-1, 2),
    lambda: aire_rectangle(2, -1),
])
def test_dimension_negative(appel):
    with pytest.raises(ValueError):
        appel()
