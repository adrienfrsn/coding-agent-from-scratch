from texte import nettoyer


def test_nettoyer():
    assert nettoyer("  Bonjour ") == "bonjour"


def test_nettoyer_none():
    assert nettoyer(None) == ""
