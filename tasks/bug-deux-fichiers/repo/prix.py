from config import TVA, REMISE_FIDELITE


def prix_ttc(prix_ht):
    return round(prix_ht * (1 + TVA), 2)


def prix_fidelite(prix_ht):
    return prix_ttc(prix_ht * (1 - REMISE_FIDELITE))
