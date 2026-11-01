from calendrier import est_bissextile


def test_bissextile_simple():
    assert est_bissextile(2024)


def test_non_bissextile():
    assert not est_bissextile(2023)


def test_siecle():
    assert not est_bissextile(1900)


def test_siecle_multiple_400():
    assert est_bissextile(2000)
