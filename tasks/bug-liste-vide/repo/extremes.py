def maximum(valeurs):
    """Plus grande valeur, ou None si la liste est vide."""
    resultat = valeurs[0]
    for v in valeurs:
        if v > resultat:
            resultat = v
    return resultat
