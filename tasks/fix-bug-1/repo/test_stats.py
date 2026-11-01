from stats import moyenne, mediane


def test_moyenne():
    assert moyenne([1, 2, 3]) == 2


def test_moyenne_liste_vide():
    assert moyenne([]) == 0


def test_mediane_impaire():
    assert mediane([3, 1, 2]) == 2


def test_mediane_paire():
    assert mediane([1, 2, 3, 4]) == 2.5