from extremes import maximum


def test_maximum():
    assert maximum([3, 9, 2]) == 9


def test_maximum_negatifs():
    assert maximum([-5, -2, -9]) == -2


def test_maximum_vide():
    assert maximum([]) is None
