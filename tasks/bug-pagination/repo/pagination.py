def page(elements, numero, taille):
    """Renvoie la page `numero` (la première page est la 1)."""
    debut = numero * taille
    return elements[debut:debut + taille]


def nombre_pages(elements, taille):
    return len(elements) // taille
