import math

import pytest

from shapes import square_area, circle_area, rectangle_area


def test_areas():
    assert square_area(3) == 9
    assert rectangle_area(2, 5) == 10
    assert circle_area(1) == pytest.approx(math.pi)


@pytest.mark.parametrize("call", [
    lambda: square_area(-1),
    lambda: circle_area(-1),
    lambda: rectangle_area(-1, 2),
    lambda: rectangle_area(2, -1),
])
def test_negative_dimension(call):
    with pytest.raises(ValueError):
        call()
