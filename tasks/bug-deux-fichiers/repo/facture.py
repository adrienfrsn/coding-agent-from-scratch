from prix import prix_ttc


def total(lignes):
    """lignes : liste de (prix_ht, quantite)."""
    return round(sum(prix_ttc(p) * q for p, q in lignes), 2)
