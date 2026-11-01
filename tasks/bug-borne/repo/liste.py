def derniers(valeurs, n):
    """Renvoie les n derniers éléments."""
    return valeurs[len(valeurs) - n + 1:]


def premiers(valeurs, n):
    """Renvoie les n premiers éléments."""
    return valeurs[:n]
