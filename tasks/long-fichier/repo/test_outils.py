from outils import ajouter_1, ajouter_60, percentile


def test_ajouter():
    assert ajouter_1(1) == 2
    assert ajouter_60(1) == 61


def test_percentile_mediane():
    assert percentile([1, 2, 3, 4, 5], 50) == 3


def test_percentile_max():
    assert percentile([1, 2, 3, 4, 5], 100) == 5


def test_percentile_min():
    assert percentile([1, 2, 3, 4, 5], 0) == 1
