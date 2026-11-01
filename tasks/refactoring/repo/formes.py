import math


def aire_cercle(rayon):
    if rayon < 0:
        raise ValueError("dimension négative")
    return math.pi * rayon ** 2


def aire_carre(cote):
    if cote < 0:
        raise ValueError("dimension négative")
    return cote ** 2


def aire_rectangle(largeur, hauteur):
    if largeur < 0 or hauteur < 0:
        raise ValueError("dimension négative")
    return largeur * hauteur
