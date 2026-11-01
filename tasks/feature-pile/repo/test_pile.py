import pytest

from pile import Pile


def test_depiler():
    p = Pile()
    p.empiler(1)
    p.empiler(2)
    assert p.depiler() == 2
    assert p.depiler() == 1


def test_sommet():
    p = Pile()
    p.empiler(7)
    assert p.sommet() == 7
    assert len(p) == 1


def test_depiler_vide():
    with pytest.raises(IndexError):
        Pile().depiler()


def test_est_vide():
    p = Pile()
    assert p.est_vide()
    p.empiler(1)
    assert not p.est_vide()
