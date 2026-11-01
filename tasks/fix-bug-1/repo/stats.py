def moyenne(valeurs):
    if not valeurs:
        return 0
    return sum(valeurs) / len(valeurs)


def mediane(valeurs):
    tri = sorted(valeurs)
    milieu = len(tri) // 2
    if len(tri) % 2 == 0:
        return (tri[milieu] + tri[milieu + 1]) / 2
    return tri[milieu]