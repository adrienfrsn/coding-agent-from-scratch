from facture import total
from prix import prix_ttc, prix_fidelite


def test_prix_ttc():
    assert prix_ttc(100) == 120


def test_prix_fidelite():
    assert prix_fidelite(100) == 114


def test_total():
    assert total([(100, 2), (50, 1)]) == 300
