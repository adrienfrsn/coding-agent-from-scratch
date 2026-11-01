from liste import derniers, premiers


def test_derniers():
    assert derniers([1, 2, 3, 4, 5], 2) == [4, 5]


def test_derniers_tout():
    assert derniers([1, 2], 2) == [1, 2]


def test_premiers():
    assert premiers([1, 2, 3], 2) == [1, 2]
